# events/forms.py

from django import forms
from .models import Event, Material

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
