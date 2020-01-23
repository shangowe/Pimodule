from .models import Module

from rest_framework import serializers

class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Module
        fields =['nms_server','name','btsstatus','hvacstatus','txnstatus']

class SimpleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    btsstatus = serializers.BooleanField()
    hvacstatus= serializers.BooleanField()


