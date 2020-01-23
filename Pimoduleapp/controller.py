from .models import Module
from .httpsender import Sender


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

class ModuleController(ModuleMixin):

    def sendhello(self):
        """
        Method to check the transmission status for the site by requsting from the NMS http://nsm_server/checktxn

        :return: {"TXN":"True"} or {"TXN":"False"}
        """
        endpoint = 'http://{0}/checktxn'.format(self.module.nms_server) # Cconstruct the endpoint to send to NMS server
        sender = Sender() # create an http sender instance
        response = sender.sendjson(endpoint) # send the request

        return response

    def checktransmission(self):
        """
        Method to request txn station

        :return:
        """
        hello = self.sendhello()
        if hello['TXN'] == 'False':
            print('TXN is offline')
            return False
        elif hello['TXN'] == 'True':
            print('TXN is online')
            return True
        else :
            return False










