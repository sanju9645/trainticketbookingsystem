from django import forms
from .models import Agent

class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name','phone','address','profile_pic']