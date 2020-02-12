from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module
from Pimoduleapp.controller import ModuleController, BTScontroller

class Command(BaseCommand):

    help = 'set bts pin'

    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=int)
        parser.add_argument('-s', '--status', type=str, help='Set Module interface ip address')


    def handle(self, *args, **options):

        pin = options['pin'][0]
        status = options['status']

        bts = BTScontroller()
        bts.update_pin_db(pin)

        if status == 'on':
            bts.on()
        elif status == 'off':
            bts.off()
        else :
            pass




