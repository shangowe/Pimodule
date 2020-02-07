from django.core.management.base import BaseCommand, CommandError
from Pimoduleapp.models import Module

class Command(BaseCommand):

    help = 'Sets up the Powermodule settings'

    def add_arguments(self, parser):

        parser.add_argument('name', nargs='+', type=str)

        parser.add_argument('-n','--nms',type=str,help='Set NMS server ip address')
        parser.add_argument('-i','--if',type=str,help='Set Module interface ip address')
        parser.add_argument('-m','--netmask',type=str,help='Set Module interface mask')

    def handle(self, *args, **options):

        name = options['name'][0]
        nms_server = options['nms']
        ip = options['if']


        module = Module(name=name,nms_server=nms_server,id=1,IP=ip)
        module.save()

