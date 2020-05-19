from django import forms
from .models import Module

class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields =('nms_server','IP','name','hvac_pin','bts_pin','mains_pin','gen_pin')