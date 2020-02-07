from django.test import TestCase
from .views import PMI
from .models import Module
from .controller import HVACcontroller, BTScontroller, ModuleController, ConfigManager

# Create your tests here.

class TestPMI(TestCase):

    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()

    def testMode(self):
        pmi = PMI()
        mod = pmi.mod

        self.assertEqual('MOD5',mod.name)


class TestHVACcontroler(TestCase):
    """
    Test the HVACcontroller implementation
    """

    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.hvac = HVACcontroller()

    def testHVACStatus(self):

        """
        Test the status property for HVAC and the update_status_db method
        :return:
        """
        self.hvac.update_status_db(False)
        self.assertEqual(False,self.hvac.status)

    def testsetGPIO(self):
        self.hvac.updateGPIO(1, False) # set pin for HVAC and status
        self.assertEqual(False,self.hvac.status)
        self.assertEqual(1,self.hvac.pin)

    def testOn(self):
        self.hvac.update_pin_db(3)
        self.hvac.on()
        self.hvac.off()

class TestBTScontroler(TestCase):
    """
    Test the BTScontroller implementation
    """
    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.bts = BTScontroller()

    def testHVACStatus(self):
        self.bts.update_status_db(False)
        self.assertEqual(False,self.bts.status)

    def testsetGPIO(self):
        self.bts.updateGPIO(1, False) # set pin for bts and status
        self.assertEqual(False,self.bts.status)
        self.assertEqual(1,self.bts.pin)

    def testOn(self):
        self.bts.update_pin_db(3)
        self.bts.on()
        self.bts.off()

class TestModuleController(TestCase):
    """
    Test the ModuleController implementation
    """
    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.modctl = ModuleController()

    def testsavename(self):
        print(self.modctl.module.id)
        self.modctl.setname('New')
        print(self.modctl.module.name)

    def testsetnms(self):
        print(self.modctl.module.id)
        self.modctl.setnms('127.0.0.1:8080')
        print(self.modctl.module.nms_server)

    def testBTSproperty(self):
        self.bts = BTScontroller()
        self.hvac = HVACcontroller()
        self.bts.update_status_db(True)
        self.hvac.update_status_db(True)
        self.assertEqual(True,self.modctl.BTS)
        self.assertEqual(True,self.modctl.HVAC)


class TestModuleHelloUpdates(TestCase):
    """
    Test the sending of the Hello Updates to the NMS.
    """
    def setUp(self):
        self.modctl = ModuleController()

    def testsendHello_withdata(self):
        data = {'module': '192.168.1.1', 'BTS': 'True', 'HVAC': True, 'name':'Himal'}
        reply = self.modctl.sendhello(data)
        reply = reply.content.decode('utf-8')
        print(reply)

    def testdefaultHello(self):
        reply = self.modctl.sendhello()
        reply = reply.content.decode('utf-8')
        print(reply)

    def testchecktransmission(self):
        self.modctl.checktransmission() # test transmission

class TestConfigManager(TestCase):

    def testdata(self):
        config = ConfigManager()
        data = config.data()
        print(data)

    def testname(self):
        config = ConfigManager()
        print('name: ',config.name)

    def testgenerator(self):
        config = ConfigManager()
        print('generator: ',config.generator)

    def testbattery(self):
        config = ConfigManager()
        print('battery: ',config.battery)

    def testsetname(self):
        conf = ConfigManager()
        conf.set_name('Mega')

        newconf = ConfigManager()
        self.assertEqual('Mega', newconf.name)

    def testsetgenerator(self):
        conf = ConfigManager()

        conf.set_generator('Y')
        newconf = ConfigManager()
        self.assertEqual('Y', newconf.generator)

        conf2 = ConfigManager()
        conf2.set_generator(False)
        newconf2 = ConfigManager()
        self.assertEqual(False, newconf2.generator)

        conf = ConfigManager()

        conf.set_generator('Y')
        newconf = ConfigManager()
        self.assertEqual('Y', newconf.generator)












