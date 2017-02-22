from unittest import TestCase
from helper import handle_uploaded_file, compute_los
import csv


class LosComputationTest(TestCase):
    def compute_los_test(self):
        myfile = open('seed.csv', 'w+')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(["12/1/2016", "12/1/2016", "Bob", "A"])
        wr.writerow(["12/2/2016", "12/5/2016", "Rich", "D"])
        wr.writerow(["12/3/2016", "12/7/2016", "Rich", "D"])
        wr.writerow(["12/4/2016", "12/5/2016", "Rich", "A"])
        wr.writerow(["12/4/2016", "12/6/2016", "Simone", "E"])
        myfile.close()
        myfile = open('seed.csv', 'rb')
        handle_uploaded_file(myfile)
        expected_output = [{'average_los': 1,
                            'mechanic': 'Bob',
                            'ratio_of_average': 1,
                            'repair_type': 'A'},
                           {'average_los': 2,
                            'mechanic': 'Rich',
                            'ratio_of_average': 0.5,
                            'repair_type': 'A'},
                           {'average_los': 4,
                            'mechanic': 'Rich',
                            'ratio_of_average': 0.5,
                            'repair_type': 'D'},
                           {'average_los': 3,
                            'mechanic': 'Simone',
                            'ratio_of_average': 1,
                            'repair_type': 'E'}]

        output_data = compute_los()

        self.assertEqual(output_data, expected_output)
