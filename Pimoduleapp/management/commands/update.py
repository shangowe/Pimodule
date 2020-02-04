from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.controller import ModuleController

class Command(BaseCommand):

    help = 'Sets up the Powermodule settings'

    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=str)

        parser.add_argument('-n','--nms',type=str,help='Set NMS server ip address')
        parser.add_argument('-i','--if',type=str,help='Set Module interface ip address')
        parser.add_argument('-m','--nemask',type=str,help='Set Module interface IP address')

    def handle(self, *args, **options):

        name = options['name'][0]
        nms_server = options['nms']
        print(name)

        mctl = ModuleController()
        mctl.setname(name)
        mctl.setnms(nms_server)