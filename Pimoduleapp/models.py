from django.db import models

# Create your models here.
class Module(models.Model):
    """
    A model to represent the NMS details
    """
    nms_server = models.CharField(max_length=20) # the ipaddress for the NMS
    IP = models.CharField(max_length=20,null=True) # the ipaddress for the NMS
    name = models.CharField(max_length=200)
    btsstatus = models.BooleanField(default=False)
    hvacstatus = models.BooleanField(default=False)
    txnstatus = models.BooleanField(default=False) # transmission link status value
    hvac_pin = models.IntegerField(verbose_name='HVAC-PIN', null=True) # GPIO pin for raspberry pi connected to hvac relay
    bts_pin=models.IntegerField(verbose_name='BTS-PIN', null=True) # GPIO pin for raspberry pi connected to bts relay

