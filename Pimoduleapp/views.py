from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .serializers import ModuleSerializer
from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Module
from .serializers import ModuleSerializer, SimpleSerializer
from .controller import *
from rest_framework import permissions


# Create your views here.


class PMI(object):

    @property
    def mod(self):
        return Module.objects.get(id=1)


class ModuleViewSet(viewsets.ModelViewSet):
    """
    A class to view the module settings via api
    the view exposes the module information stored in the database on the module
    """
    power_module = PMI()
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleData(APIView,ModuleMixin):
    """
    List module details from the db
    """

    def get(self,request,format=None):
        """

        :param request:
        :param format:
        :return:
        """
        power_module = PMI()
        queryset = power_module.mod
        data = SimpleSerializer(queryset)
        # serializer_class = ModuleSerializer

        return Response(data.data)

class SetupView(TemplateView):
    """
    Generic view to configure the module via a web interface
    """
    template_name = 'Powermoduleapp/setup.html'


    def get_context_data(self, **kwargs):
        context = super(SetupView,self).get_context_data(**kwargs)
        power_module = PMI() # create power module instance from db
        module_entry = power_module.mod
        context['module'] = module_entry
        return context



class BTSOFF(APIView):
    """
    API view to switch of BTS
    """

    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        bts = BTScontroller()
        bts.off()
        response={"bts":"","success":"true"}
        response['bts'] = bts.status
        return Response(response)


class BTSON(APIView):
    """
    API view to switch on BTS
    """
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        bts = BTScontroller()
        bts.on()
        #TODO add logic to set success value in response
        response={"bts":"","success":""}
        response['bts'] = bts.status
        return Response(response)


class HVACOFF(APIView):
    """
    API view to switch of BTS
    """
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):

        hvac = HVACcontroller()
        hvac.off()
        response = {"hvac-status": ""}
        response['hvac-status'] = hvac.status
        return Response(response)


class HVACON(APIView):
    """
    API view to switch of BTS
    """
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        hvac = HVACcontroller()
        hvac.on()
        response={"hvac-status":""}
        response['hvac-status'] = hvac.status
        return Response(response)

class GENOFF(APIView):
    """
    API view to switch off GEN
    """
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):

        gen = GENcontroller()
        gen.off()
        response = {"gen-status": ""}
        response['gen-status'] = gen.status
        return Response(response)

class GENON(APIView):
    """
    API view to switch on Generator
    """
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        gen = GENcontroller()
        gen.on()
        response={"gen-status":""}
        response['gen-status'] = gen.status
        return Response(response)


class BTS(APIView):
    """
    To return the current status of the BTS switch
    """

    def get(self,request):
        bts = BTScontroller()
        response={"btsstatus":""}
        response['btsstatus'] = bts.status
        return Response(response)


class HVAC(APIView):
    """
    To return the current status of the HVAC switch
    """

    def get(self,request):

        hvac = HVACcontroller()
        response={"hvacstatus":hvac.status}
        return Response(response)

class GEN(APIView):
    """
    To return the current status of the GEN switch
    """

    def get(self,request):

        gen = GENcontroller()
        response={"genstatus":gen.status}
        return Response(response)








