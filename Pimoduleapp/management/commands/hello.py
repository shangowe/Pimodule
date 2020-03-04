from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module
from Pimoduleapp.controller import ModuleController, BTScontroller, HVACcontroller
import logging

bts = BTScontroller()
hvac = HVACcontroller()


def turn_equipment_on():
    bts.on()
    hvac.on()

def turn_equipment_off():
    bts.off()
    hvac.off()

class Command(BaseCommand):

    help = 'send hello'


    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=str)

        parser.add_argument('-n','--nms',type=str,help='Set NMS server ip address')
        parser.add_argument('-i','--if',type=str,help='Set Module interface ip address')
        parser.add_argument('-m','--netmask',type=str,help='Set Module interface mask')

    def handle(self, *args, **options):

        name = options['name'][0]
        nms_server = options['nms']
        ip = options['if']

        ctl = ModuleController()
        txn_state = ctl.checktransmission()
        logging.getLogger('hello').info('sent hello: {0}, transmission status is {1}'.format(ctl.name,txn_state))

        self.runchecks(txn_state) # run the routine check for transmission status



    def runchecks(self,txn_is_ok):
        ctl = ModuleController()


        if txn_is_ok:
            logging.getLogger('hello').info('sent hello: {0}, transmission status is {1}'.format(ctl.name, txn_is_ok))

            if 0 < ctl.TXN_OFF_COUNTER < 6 :
                # reset the counter for transmission


                if ctl.TXN_ON_COUNTER < 2:
                    # check if the switch on delay is in overflow or not
                    ctl.increament_txn_on_counter()
                    logging.getLogger('hello').info(
                        'TXN_OFF_COUNTER: {0}, TXN_ON_COUNTER : {1}, transmission status is {2}'.format(
                            ctl.TXN_OFF_COUNTER,ctl.TXN_ON_COUNTER, txn_is_ok))


                elif ctl.TXN_ON_COUNTER == 2:
                    logging.getLogger('hello').info(
                        ' SWITCHING-OFF @ TXN_OFF_COUNTER: {0}, TXN_ON_COUNTER : {1}, transmission status is {2}'.format(
                            ctl.TXN_OFF_COUNTER,ctl.TXN_ON_COUNTER, txn_is_ok))
                    ctl.reset_txn_on_counter()
                    ctl.reset_txn_off_counter()
                    turn_equipment_on()

            elif ctl.TXN_OFF_COUNTER == 6:
                # the counter is in overflow

                if ctl.TXN_ON_COUNTER < 2:
                    # check if the switch on delay is in overflow or not
                    ctl.increament_txn_on_counter()
                    logging.getLogger('hello').info(
                        ' DO nothing no overflow @ TXN_OFF_COUNTER: {0}, TXN_ON_COUNTER : {1}, transmission status is {2}'.format(
                            ctl.TXN_OFF_COUNTER,ctl.TXN_ON_COUNTER, txn_is_ok))

                elif ctl.TXN_ON_COUNTER == 2:
                    # switch on the equipment and reset all counters
                    ctl.reset_txn_on_counter()
                    ctl.reset_txn_off_counter()
                    turn_equipment_on()
                    logging.getLogger('hello').info(
                        ' SWITCHING-ON @ TXN_OFF_COUNTER: {0}, TXN_ON_COUNTER : {1}, transmission status is {2}'.format(
                            ctl.TXN_OFF_COUNTER,ctl.TXN_ON_COUNTER, txn_is_ok))


            else:
                pass



        else :

            if 0 < ctl.TXN_OFF_COUNTER < 6 :
                ctl.increament_txn_off_counter()
                ctl.reset_txn_on_counter()

            elif ctl.TXN_OFF_COUNTER == 6:
                # keep the on counter in reset mode
                ctl.reset_txn_on_counter()
                turn_equipment_off()


            else:
                pass




