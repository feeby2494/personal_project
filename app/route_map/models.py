from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

# Brand choices:
brands = [
    ("ap", "Apple"),
    ("ss", "Samsung"),
    ("ms", "Microsoft"),
    ("gg", "Google"),
]

# US state choices:
states = [
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District of Columbia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
]


# Create your models here.
User = get_user_model()

# customer is just a User and belongs to the "customer group"
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # link every customer to a user
    # usa_addresses customer can have multiple addresses, don't have to difine this relationship in Django
    # workorders
    # devices
    # make into group of "customers"
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], default="0000000000")
    phone_country_code = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')], default="000")

    def __str__(self):
        return f"{self.user.get_username()}"


    # have addressess that will give info for points on the map
class UsaAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    first_line = models.CharField(max_length=90)
    second_line = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=2, choices=states) # state two character abriviation
    postal_code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.first_line} {self.second_line} {self.city}, {self.state} {self.postal_code}"


#"""
#
# Static Constants
#
#"""  
class Brand(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=65)
    model_number = models.CharField(max_length=65, null=True)

    def __str__(self):
        return self.name


# device is an individual device that can have multiple jobs, depending on how many times it comes back for repair
class Device(models.Model):
    # work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    serial = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.serial

class RepairType(models.Model):
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class PartNumber(models.Model):
    device = models.ManyToManyField(RepairType)
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

#"""
#
# Work Flow
#
#"""

# work order is a group of jobs linked to devices that a user submits for pick up or shipping
    # will show all work orders that need to be picked up or dropped off on map
class WorkOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(UsaAddress, on_delete=models.SET_NULL, null=True) # if customer deletes address tied to a work order, then will need to ask them to edit address or do so in admin console

    def __str__(self):
        return f"{self.id}: {self.customer.user.get_username}"

# job is a single device that is apart of a work order; since the same device can come back again as a new repair, we do not directly put devices on work order 
class Repair(models.Model):
    delivery_methods = [("LO", "local"), ("EX", "Express Shipping"), ("NO", "Normal Shipping")]

    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    delivery = models.CharField(max_length=2, choices=delivery_methods) # shipping page will denote a work order as express or not; local orders will show up on map when admin is logged in

    def __str__(self):
        return f"{self.work_order.id}: {self.device.serial}"
#"""
#
# Dynamic Inventory and Parts
#
#"""

# Connects parts from static inventory to work flow
class InventoryLocation(models.Model):
    pass



#"""
#
# Accounting
#
#"""

# PO is for buying
class PurchaseOrder(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.TextField(max_length=256, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    paypal_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

# SO is for sellings
class SalesOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.TextField(max_length=256, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


#"""
#
# Connectors
#
#"""

# One job can have multiple repair instances; Also a repair can 
class Job(models.Model):
    repair_type = models.ForeignKey(RepairType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=65)




class PartInstance(models.Model):
    part_number = models.ForeignKey(PartNumber, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(InventoryLocation, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)
    broken_by_tech = models.BooleanField()

class ShipOrder(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)



