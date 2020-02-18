from .models import Module
from .httpsender import Sender
import yaml, json
import Pimodule.settings as setting
import RPi.GPIO as GPIO

# an import of the dummy GPIO library
# from .RPI import GPIO


def create_default_module():
    """
    Method to create a default module with default settings
    :return:
    """
    default_nms_server = '192.168.1.1'
    default_module_name = 'Default'

    # create the module model
    module = Module.objects.create(nms_server=default_nms_server, name=default_module_name,id=1)

    return module


class ModuleMixin:


    # GPIO.BOARD -- Board numbering scheme. The pin numbers follow the pin numbers on header P1.
    # GPIO.BCM -- Broadcom chip-specific pin numbers. These pin numbers follow the lower-level numbering system
    GPIO.setmode(GPIO.BCM)

    try:
        # Try get a module for the object with ID = 1
        module = Module.objects.get(id=1)

    except Module.DoesNotExist:

        # Handle exception of Module not exist
        module = create_default_module()



    def getModule(self):
        return self.module

    def setGPIO(self,pin,status):
        """
        Method to set the pin for Raspeberry pi hi or low, this module implements the GPIO library for raspberry pi
        :return:
        """
        #TODO: add RPi.GPIO implemantion here
        GPIO.setup(pin, GPIO.OUT)
        if status:
            # set pin to high
            GPIO.output(pin, GPIO.HIGH)
        else:
            # set pin to LOW
            GPIO.output(pin,GPIO.LOW)

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
        # set the pin as an output for the pi
        GPIO.setup(pin, GPIO.OUT)

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
        Method to update the status of the bts in the module db

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
        # set the pin as an output for the pi
        GPIO.setup(pin, GPIO.OUT)

        self.getModule().bts_pin = pin
        self.getModule().save(update_fields=['bts_pin'])


    @property
    def status(self):
        return self.module.btsstatus

    @property
    def pin(self):
        return self.module.bts_pin


class ModuleController(ModuleMixin):

    def sendhello(self,*data):
        """
        Method to check the transmission status for the site by requsting from the NMS http://nsm_server/checktxn

        :return: {"TXN":"True"} or {"TXN":"False"}
        """
        endpoint = 'http://{0}/hello/'.format(self.nms) # Construct the endpoint to send to NMS server
        sender = Sender() # create an http sender instance
        if data:
            response = sender.sendjson(endpoint, *data)  # send the request
        else:
            data = self.generatehellodata() # generate data from the db
            response = sender.sendjson(endpoint, data)  # send the request



        return response


    def generatehellodata(self):
        """
        Generates a dict for sending to the NMS as a hello

        :return:
        """
        data ={}
        data['BTS']=self.BTS
        data['HVAC']=self.HVAC
        data['module']=self.IP
        data['name']=self.name
        return data

    def checktransmission(self):
        """
        Method to request txn station and check status. This method should be called routinely to confirm transmission
        status for the site.
        :return:
        """
        try:
            reply = self.sendhello()
            hello = reply.content.decode('utf-8') # decode the JSON respnse from NMS
            hello = json.loads(hello)
        except :
            hello = {'ACK':'NOK'}

        if hello['ACK'] == 'ER':
            print('TXN is okay but an error occured on the server')
            return False
        elif hello['ACK'] == 'OK':
            print('TXN is online')
            return True
        else :
            print('TXN is offline')
            return False


    def setname(self,name):
        """
        Method to set the name of the Module in the database

        :return:
        """
        self.getModule().name = name
        self.getModule().save(update_fields=['name'])


    def setnms(self,ipaddress):
        """
        Configure the nms details for the module
        :param name:
        :return:
        """
        self.getModule().nms_server = ipaddress
        self.getModule().save(update_fields=['nms_server'])

    def setip(self,ip):
        """
        Configure the module ip address for the device

        :param ip: IP address of the module
        :return:
        """
        self.getModule().IP = ip
        self.getModule().save(update_fields=['IP'])

    def increament_txn_off_counter(self):
        """
        Increments the counter for TXN off by one step

        :return:
        """
        current_value = self.TXN_OFF_COUNTER
        current_value = current_value+1

        self.getModule().txn_offline_counter = current_value
        self.getModule().save(update_fields=['txn_offline_counter'])

    def increament_txn_on_counter(self):
        """
        Increments the counter for TXN on by one step

        :return:
        """
        current_value = self.TXN_ON_COUNTER
        current_value = current_value+1

        self.getModule().txn_online_counter = current_value
        self.getModule().save(update_fields=['txn_online_counter'])

    def reset_txn_off_counter(self):
        """
        Method to rest the counter for txn offline status
        :return:
        """
        self.getModule().txn_offline_counter = 0
        self.getModule().save(update_fields=['txn_offline_counter'])

    def reset_txn_on_counter(self):
        """
        Method to rest the counter for txn online status
        :return:
        """
        self.getModule().txn_online_counter = 0
        self.getModule().save(update_fields=['txn_online_counter'])



    @property
    def BTS(self):
        return self.getModule().btsstatus

    @property
    def HVAC(self):
        return self.getModule().hvacstatus

    @property
    def IP(self):
        return self.getModule().IP

    @property
    def name(self):
        return self.getModule().name

    @property
    def nms(self):
        return self.getModule().nms_server

    @property
    def TXN_OFF_COUNTER(self):
        return self.getModule().txn_offline_counter

    @property
    def TXN_ON_COUNTER(self):
        return self.getModule().txn_online_counter



class ConfigManager(object):
    """
    A manger class for yaml configuations
    """

    config_file = setting.PIMODE_CONFIG # yaml cconfig file location

    def __init__(self):
        self.settings = self.data()

    def data(self):
        with open(self.config_file, 'r') as file :

            settings = yaml.load(file,Loader=yaml.FullLoader) # read config YAML file
        return settings

    def save(self):
        with open(self.config_file, 'w') as file :

            yaml.dump(self.settings, file) # save config YAML file

    def set_name(self, name):
        self.settings['module']['name']=name
        self.save()

    def set_generator(self,gen):
        self.settings['module']['generator'] = gen
        self.save()

    def set_battery(self,bat):
        self.settings['module']['battery'] = bat
        self.save()

    @property
    def name(self):

        return self.settings['module']['name']

    @property
    def generator(self):
        return self.settings['module']['generator']

    @property
    def battery(self):
        return self.settings['module']['battery']

    @property
    def nms(self):
        return self.settings['module']['nms']

















