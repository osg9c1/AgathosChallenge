from django.db import models


class ShopWorkFlowFact(models.Model):
    MECHANIC_CHOICES = ((1, "Bob"), (2, "Rich"), (3, "Larry"), (4, "Simone"), (5, "Peter"))
    REPAIR_TYPE = ((1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F'))
    MECHANIC_CHOICES_DICT = dict(MECHANIC_CHOICES)
    REPAIR_TYPE_DICT = dict(REPAIR_TYPE)
    REPAIR_TYPE_NATIONAL_AVERAGES = {1: 1, 2: 1, 3: 3, 4: 2, 5: 3, 6: 2.5}

    id = models.AutoField(primary_key=True)
    dropoff_date = models.DateField()
    pickup_date = models.DateField()
    assigned_mechanic = models.IntegerField(choices=MECHANIC_CHOICES)
    repair_type = models.IntegerField(choices=REPAIR_TYPE)
    length_of_service = models.IntegerField()
    objects = models.Manager()

    class Meta:
        app_label = 'lengthOfService'


    def delete_everything(self):
        ShopWorkFlowFact.objects.all().delete()

