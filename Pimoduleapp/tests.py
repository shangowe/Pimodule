from django.test import TestCase
from django.urls import reverse
from .views import PMI
from .models import Module
from .controller import HVACcontroller, BTScontroller, GENcontroller, ModuleController, ConfigManager, MAINScontroller
from .management.commands import hello

from rest_framework.test import APITestCase

import Pimodule.settings as settings # import the settings of the Pimodule.


# Create your tests here.

class TestPMI(TestCase):

    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()

    def testMode(self):
        pmi = PMI()
        mod = pmi.mod

        self.assertEqual('MOD5',mod.name)


class TestHVACcontroller(TestCase):
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

class TestBTScontroller(TestCase):
    """
    Test the BTScontroller implementation
    """
    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.bts = BTScontroller()

    def testBTSStatus(self):
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

class TestGENcontroller(TestCase):
    """
    Test the GENcontroller implementation
    """
    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.gen = GENcontroller()

    def testHVACStatus(self):
        self.gen.update_status_db(False)
        self.assertEqual(False,self.gen.status)

    def testsetGPIO(self):
        self.gen.updateGPIO(1, False) # set pin for bts and status
        self.assertEqual(False,self.gen.status)
        self.assertEqual(1,self.gen.pin)

    def testOn(self):
        self.gen.update_pin_db(3)
        self.gen.on()
        self.gen.off()
class TestMAINScontroller(TestCase):
    """
    Test the Mainscontroller implementation
    """
    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.mains = MAINScontroller()

    def testMAINSStatus(self):
        self.mains.update_status_db(False)
        self.assertEqual(False,self.mains.status)

    def testcheckstatus(self):
        self.mains.check_state()
        self.assertEqual(True, self.mains.status)



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
        self.gen = GENcontroller()
        self.bts.update_status_db(True)
        self.hvac.update_status_db(True)
        self.gen.update_status_db(False)
        self.assertEqual(True,self.modctl.BTS)
        self.assertEqual(True,self.modctl.HVAC)
        self.assertEqual(False,self.modctl.GEN)

    def testBTSPinConfiguration(self):

        self.modctl.configure_bts_pin(11) # assign the bts pin of the module

        self.assertEqual(self.modctl.btspin,11)

    def testHVACPinConfiguration(self):

        self.modctl.configure_hvac_pin(11) # assign the hvac pin of the module

        self.assertEqual(self.modctl.hvacpin,11)

    def testreset_txn_off_counter(self):

        self.modctl.reset_txn_off_counter()
        print(self.modctl.TXN_OFF_COUNTER)

    def test_increament_txn_off_counter(self):

        self.modctl.reset_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.assertEqual(2,self.modctl.TXN_OFF_COUNTER)
        self.modctl.reset_txn_off_counter()
        self.assertEqual(0, self.modctl.TXN_OFF_COUNTER)

    def test_increament_txn_on_counter(self):

        self.modctl.reset_txn_on_counter()
        self.modctl.increament_txn_on_counter()
        self.modctl.increament_txn_on_counter()
        self.assertEqual(2,self.modctl.TXN_ON_COUNTER)
        self.modctl.reset_txn_on_counter()
        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)

class TestModuleHelloUpdates(TestCase):
    """
    Test the sending of the Hello Updates to the NMS.
    """
    def setUp(self):
        self.modctl = ModuleController()

    def testsendHello_withdata(self):
        data = {'module': '192.168.1.1:8080', 'BTS': 'True', 'HVAC': True, 'name':'Himal'}
        reply = self.modctl.sendmsg(self.modctl.HELLO,data)
        reply = reply.content.decode('utf-8')
        expected_reply = {'ACK': 'OK', 'BTS': True, 'GEN': None, 'HVAC': True, 'MAINS': None}
        self.assertJSONEqual(reply,expected_reply)


    def testdefaultHello(self):
        reply = self.modctl.sendmsg(self.modctl.HELLO)
        reply = reply.content.decode('utf-8')
        expected_reply = {"BTS": None, "ACK": "ER", "HVAC": None}
        self.assertJSONEqual(reply,expected_reply)

    def testchecktransmission(self):
        self.modctl.checktransmission() # test transmission

class TestConfigManager(TestCase):

    def testdata(self):
        config = ConfigManager()
        data = config.data
        expected_data = {'module': dict(ip=None, name='Mega', generator={'status': 0, 'pin': 18, 'set': 'Y'},
                                        bts={'status': 1, 'pin': 21}, battery={'status': 1, 'pin': 19, 'set': 0},
                                        nms='192.168.1.2:8080', mains={'status': 0, 'pin': 17},
                                        hvac={'status': 1, 'pin': 20})}

        self.assertDictEqual(data, expected_data)

    def testname(self):
        config = ConfigManager()
        self.assertEqual('Mega',config.name)


    def testgenerator(self):
        config = ConfigManager()
        expected_dict = {'status': 0, 'pin': 18, 'set': 'Y'}
        self.assertDictEqual(expected_dict, config.generator)

    def testbattery(self):
        config = ConfigManager()
        expected_dict =  {'pin': 19, 'status': 1, 'set': 0}
        self.assertDictEqual(expected_dict, config.battery)

    def testsetname(self):
        conf = ConfigManager()
        conf.set_name('Mega')

        newconf = ConfigManager()
        self.assertEqual('Mega', newconf.name)

    def testsetgenerator(self):
        conf = ConfigManager()

        conf.set_generator('Y')
        newconf = ConfigManager()
        expected_dict = dict(set='Y', pin=18, status=0)
        self.assertEqual(expected_dict, newconf.generator)

        conf2 = ConfigManager()
        conf2.set_generator(False)
        newconf2 = ConfigManager()
        expected_dict = dict(set=False, pin=18, status=0)
        self.assertDictEqual(expected_dict, newconf2.generator)

        conf = ConfigManager()

        conf.set_generator('Y')
        newconf = ConfigManager()
        expected_dict = dict(set='Y', pin=18, status=0)
        self.assertEqual(expected_dict, newconf.generator)

class TestCommands(TestCase):
    """
    Test the methods defined the commands module
    """
    def setUp(self):

        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.modctl = ModuleController()
        self.modctl.reset_txn_off_counter()
        self.modctl.reset_txn_on_counter()

        # if running on Pi need to set up actuall ins for bts and hvac or else GPIO exceptions are raised
        if settings.RASPI == True:
            self.modctl.configure_bts_pin(11)
            self.modctl.configure_hvac_pin(12)




    def test_runchecks_with_overflow_txok(self):
        """
        Test the runchecks method from the  hello management commnad.

        :return:
        """
        command = hello.Command()

        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()

        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6, self.modctl.TXN_OFF_COUNTER)

        i = 0
        while i < 2:
            command.runchecks(True)
            i+=1

        self.assertEqual(2, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6,self.modctl.TXN_OFF_COUNTER)
        command.runchecks(True)
        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(0,self.modctl.TXN_OFF_COUNTER)

    def test_runchecks_with_overflow_txnok(self):
        """
        Test the runchecks method from the  hello management commnad.

        :return:
        """
        command = hello.Command()
        module = self.modctl.getModule()

        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()

        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6, self.modctl.TXN_OFF_COUNTER)

        i = 0
        while i < 2:
            command.runchecks(False)
            i+=1

        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6,self.modctl.TXN_OFF_COUNTER)
        command.runchecks(False)
        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6,self.modctl.TXN_OFF_COUNTER)
        self.assertEqual(False,module.btsstatus)
        self.assertEqual(False,module.hvacstatus)


    def test_runchecks_before_overflow_txok(self):
        """
        Test the runchecks method from the  hello management commnad.

        :return:
        """
        command = hello.Command()
        module = self.modctl.getModule()

        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()


        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(4, self.modctl.TXN_OFF_COUNTER)

        i = 0
        while i < 2:
            command.runchecks(True)
            i+=1

        self.assertEqual(2, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(4,self.modctl.TXN_OFF_COUNTER)
        command.runchecks(True)
        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(0,self.modctl.TXN_OFF_COUNTER)
        self.assertEqual(True,module.btsstatus)
        self.assertEqual(True,module.hvacstatus)

    def test_runchecks_before_overflow_txnok(self):
        """
        Test the runchecks method from the  hello management commnad.

        :return:
        """
        command = hello.Command()

        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()
        self.modctl.increament_txn_off_counter()


        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(4, self.modctl.TXN_OFF_COUNTER)

        i = 0
        while i < 2:
            command.runchecks(False)
            i+=1

        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6,self.modctl.TXN_OFF_COUNTER)
        command.runchecks(False)
        self.assertEqual(0, self.modctl.TXN_ON_COUNTER)
        self.assertEqual(6,self.modctl.TXN_OFF_COUNTER)

class TestAPI(APITestCase):

    def setUp(self):
        mod = Module(name='MOD5',nms_server='192.168.10.10')
        mod.save()
        self.modctl = ModuleController()

    def test_get_all(self):

        response = self.client.get('/getall/')
        data = {'nms_server': '192.168.10.10', 'hvacstatus': False, 'btsstatus': False, 'mainsstatus': False,
                'name': 'MOD5', 'genstatus': False, 'txnstatus': False}

        self.assertEqual(response.data, data)


    def testMAINSStatus(self):
        self.mains = MAINScontroller()
        self.mains.update_status_db(False)
        self.assertEqual(False,self.mains.status)

        # check if running on raspberry pi or on test environment
        if settings.RASPI == True:
            self.mains.update_pin_db(10)
            self.data = {'nms_server': '192.168.10.10', 'hvacstatus': False, 'btsstatus': False, 'mainsstatus': True,
                'name': 'MOD5', 'genstatus': False, 'txnstatus': False}
        else:
            self.data = {'nms_server': '192.168.10.10', 'hvacstatus': False, 'btsstatus': False, 'mainsstatus': False,
                'name': 'MOD5', 'genstatus': False, 'txnstatus': False}

        self.mains.check_state()
        response = self.client.get('/getall/')
        print(response.data)
        print(self.data)
        self.assertEqual(response.data, self.data)





















