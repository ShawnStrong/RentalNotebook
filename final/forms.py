from final.models import Property
from django import forms

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['type', 'address', 'rent', 'bedrooms', 'bathrooms', 'link', 'notes']