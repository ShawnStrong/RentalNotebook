from final.models import Property, Place
from django import forms

class TextareaInput(forms.Textarea):
    input_type = 'textarea'

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'rent', 'bedrooms', 'bathrooms', 'link', 'notes']
        widgets = {
            'notes': TextareaInput()
        }

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['type', 'address', 'notes']
        widgets = {
            'notes': TextareaInput()
        }