from django.db import models
from django.urls import reverse

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
    genstatus = models.BooleanField(default=False)
    txnstatus = models.BooleanField(default=False) # transmission link status value
    mainsstatus = models.BooleanField(default=False) # mains status value
    hvac_pin = models.IntegerField(verbose_name='HVAC-PIN', null=True) # GPIO pin for raspberry pi connected to hvac relay
    bts_pin=models.IntegerField(verbose_name='BTS-PIN', null=True) # GPIO pin for raspberry pi connected to bts relay
    gen_pin=models.IntegerField(verbose_name='GEN-PIN', null=True) # GPIO pin for raspberry pi connected to bts relay
    mains_pin=models.IntegerField(verbose_name='MAIN-PIN', null=True) # GPIO pin for raspberry pi connected to mains relay
    txn_offline_counter = models.IntegerField(verbose_name='TXN-OFF-COUNTER', null=True,default=0) # Counter for offline status
    txn_online_counter = models.IntegerField(verbose_name='TXN-ON-COUNTER', null=True,default=0) # Counter for online status

    def get_absolute_url(self):
        return reverse('Pimoduleapp:setup', kwargs={'pk': self.pk})

