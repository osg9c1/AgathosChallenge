import csv
from datetime import *
from decimal import Decimal
from numpy import random
from models import ShopWorkFlowFact
from random import randint


def random_date(start, end):
    '''
    Generates a random date between start and end
    :param start: Datetime obj
    :param end: Datetime obj
    :return: Datetime obj
    '''

    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))


def handle_uploaded_file(file):
    '''
    Reads a csv file and updates ShopWorkFlowFact with each transaction, also computing the length of service of each
    transaction and storing it in db
    :param file: File obj
    :return: error messages
    '''
    error_msg = ""
    try:

        reader = csv.reader(file)

        for row in reader:
            try:
                dropoff_date = datetime.strptime(row[0], '%m/%d/%Y').date()
                pick_update = datetime.strptime(row[1], '%m/%d/%Y').date()
                length_of_service = pick_update - dropoff_date
                _, created = ShopWorkFlowFact.objects.get_or_create(
                    dropoff_date=dropoff_date,
                    pickup_date=pick_update,
                    assigned_mechanic=ShopWorkFlowFact.MECHANIC_CHOICES_DICT.keys()[
                        ShopWorkFlowFact.MECHANIC_CHOICES_DICT.values().index(row[2])],
                    repair_type=ShopWorkFlowFact.REPAIR_TYPE_DICT.keys()[
                        ShopWorkFlowFact.REPAIR_TYPE_DICT.values().index(row[3])],
                    length_of_service=length_of_service.days + 1

                )
            except Exception as e:
                error_msg += "Error in row {0}: {1}".format(row, str(e))
                continue
    except Exception as e:
        error_msg = "Invalid File! Please upload a csv file again."
    return error_msg


def generate_csv_file(start_date, last_date, no_of_records):
    '''
    Generates random transactions, stores them in seed.csv. Picks a random mechanic and repair_type, uses random_date to
    generate a random dropoff date and add random days from 0 to national average of of repair_type and adds it to the
    dropoff date.
    :param no_of_records: No of records to be generated
    :return: seed.csv file with the generated records
    '''
    myfile = open('seed.csv', 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in range(no_of_records):
        mechanic = randint(1, 5)
        repair_type = randint(1, 6)
        dropoff_date = random_date(start_date, last_date)
        pickup_date = dropoff_date + timedelta(
            days=random.uniform(0, ShopWorkFlowFact.REPAIR_TYPE_NATIONAL_AVERAGES[repair_type]))
        wr.writerow([dropoff_date.strftime('%m/%d/%Y'), pickup_date.strftime('%m/%d/%Y'),
                     ShopWorkFlowFact.MECHANIC_CHOICES_DICT[mechanic], ShopWorkFlowFact.REPAIR_TYPE_DICT[repair_type]])
    myfile.close()
    return myfile


def compute_los():
    '''
    Computes average length of service and ratio_of_average against every mechanic and repair type
     Average Los : Searching for all records for every combination of mechanic and repair type and generating a list the
     los times. Computing total los of the list / Length of the list

     Ratio of Average: National Average for repair type / Average Los

     Ranking/Sorting the ouput list: Sorting the list first by repair type then by ratio of average (descending order)
    :return:
    '''
    mech_rt_los_list = []
    for repair_type in ShopWorkFlowFact.REPAIR_TYPE_DICT.keys():
        for mechanic in ShopWorkFlowFact.MECHANIC_CHOICES_DICT.keys():
            mech_rt_combo_list = list(ShopWorkFlowFact.objects.filter(assigned_mechanic=mechanic,
                                                                      repair_type=repair_type).values_list(
                'length_of_service', flat=True))
            if mech_rt_combo_list:
                total_length_of_service = 0
                total_length_of_service += sum(los for los in mech_rt_combo_list)
                average_length_of_service = Decimal(total_length_of_service / len(mech_rt_combo_list))
                ratio_of_average = Decimal(
                    Decimal(ShopWorkFlowFact.REPAIR_TYPE_NATIONAL_AVERAGES[repair_type]) / average_length_of_service)
                mech_rt_los_list.append({"mechanic": ShopWorkFlowFact.MECHANIC_CHOICES_DICT[mechanic],
                                         "repair_type": ShopWorkFlowFact.REPAIR_TYPE_DICT[repair_type],
                                         "average_los": average_length_of_service,
                                         "ratio_of_average": ratio_of_average})
    mech_rt_los_list = sorted(mech_rt_los_list, key=lambda k: (k["repair_type"], -k["ratio_of_average"]))

    return mech_rt_los_list


