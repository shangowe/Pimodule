from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module
from Pimoduleapp.controller import HVACcontroller

class Command(BaseCommand):

    help = 'set hvac pin'

    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=int)
        parser.add_argument('-s', '--status', type=str, help='Set Module interface ip address')


    def handle(self, *args, **options):

        pin = options['pin'][0]
        status = options['status']

        hvac = HVACcontroller()
        hvac.update_pin_db(pin)

        if status == 'on':
            hvac.on()
        elif status == 'off':
            hvac.off()
        else :
            pass

