from django.test import TestCase
from .views import PMI
from .models import Module
from .controller import HVACcontroller, BTScontroller, ModuleController
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




