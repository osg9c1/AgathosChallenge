from django.contrib import admin
from models import ShopWorkFlowFact


class ShopWorkFlowFactAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'dropoff_date', 'pickup_date', 'assigned_mechanic', 'repair_type')

    list_filter = ('repair_type', 'assigned_mechanic')

admin.site.register(ShopWorkFlowFact, ShopWorkFlowFactAdmin)