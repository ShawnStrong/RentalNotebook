from final.models import Property, Place
from django import forms

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'rent', 'bedrooms', 'bathrooms', 'link', 'notes']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['type', 'address', 'notes']