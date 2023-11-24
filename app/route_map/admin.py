from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(UsaAddress)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Device)
admin.site.register(RepairType)
admin.site.register(PartNumber)
admin.site.register(WorkOrder)
admin.site.register(Repair)
admin.site.register(InventoryLocation)
admin.site.register(PurchaseOrder)
admin.site.register(SalesOrder)
admin.site.register(Job)
admin.site.register(PartInstance)
admin.site.register(ShipOrder)