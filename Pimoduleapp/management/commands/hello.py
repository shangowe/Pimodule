from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module
from Pimoduleapp.controller import ModuleController

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
        ctl.checktransmission()



