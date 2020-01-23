from .models import Module


class ModuleMixin:
    module = Module.objects.get(id=1)

    def getModule(self):
        return self.module

    def setGPIO(self,pin,status):
        """
        Method to set the pin for Raspeberry pi hi or low, this module implements the GPIO library for raspberry pi
        :return:
        """
        #TODO: add GPIO implemantion here

        print("setting pin ",status)
        pass

    def updateGPIO(self, pin, status):
        """
        Method to change the status of the  pin on the db on raspberry pi module.

        :param pin: HVAC pin number

        :param status: Hi or Low

        :return:
        """

        self.update_pin_db(pin) # set pin
        self.update_status_db(status) # set status



    def on(self):

        """
        Turn on pin on raspberry pi
        :return:
        """
        pin = self.pin
        self.setGPIO(pin,1)
        self.updateGPIO(pin,True)


    def off(self):

        """
        Turn on pin on raspberry pi
        :return:
        """
        pin = self.pin # get  pin
        self.setGPIO(pin,0) # set pin low
        self.updateGPIO(pin, False)



class HVACcontroller(ModuleMixin):
    """
    HVAC class object
    """
    # mod = Module.objects.get(id=1)

    def update_status_db(self, status):
        """
        Method to update the status of the hvac in the module db

        :return: None
        """

        self.getModule().hvacstatus = status
        self.getModule().save(update_fields=['hvacstatus'])

    def update_pin_db(self, pin):
        """
        Method to update the pin of the hvac in the module db
        :param pin:
        :return:
        """
        self.getModule().hvac_pin = pin
        self.getModule().save(update_fields=['hvac_pin'])


    @property
    def status(self):
        return self.module.hvacstatus

    @property
    def pin(self):
        return self.module.hvac_pin

class BTScontroller(ModuleMixin):
    """
    BTS class object
    """
    # mod = Module.objects.get(id=1)

    def update_status_db(self, status):
        """
        Method to update the status of the hvac in the module db

        :return: None
        """

        self.getModule().btsstatus = status
        self.getModule().save(update_fields=['btsstatus'])

    def update_pin_db(self, pin):
        """
        Method to update the pin of the hvac in the module db
        :param pin:
        :return:
        """
        self.getModule().bts_pin = pin
        self.getModule().save(update_fields=['bts_pin'])


    @property
    def status(self):
        return self.module.btsstatus

    @property
    def pin(self):
        return self.module.bts_pin





