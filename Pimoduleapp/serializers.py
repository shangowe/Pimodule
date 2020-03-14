from .models import Module

from rest_framework import serializers

class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Module
        fields =['nms_server','name','btsstatus','hvacstatus','genstatus','txnstatus']

class SimpleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    btsstatus = serializers.BooleanField()
    hvacstatus= serializers.BooleanField()
    genstatus= serializers.BooleanField()
    txnstatus= serializers.BooleanField()
    nms_server= serializers.CharField(max_length=200)


