from django import forms
from .models import *

class EquipmentRequestForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = ['request']