from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module
from Pimoduleapp.controller import ModuleController, BTScontroller

class Command(BaseCommand):

    help = 'set bts pin'

    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=int)


    def handle(self, *args, **options):

        pin = options['pin'][0]

        bts = BTScontroller()
        bts.update_pin_db(pin)



