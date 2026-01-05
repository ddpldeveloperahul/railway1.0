from django import forms
from django.core.exceptions import ValidationError

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload Image")

    pole_name = forms.CharField(
        label="Pole Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    temperature = forms.FloatField(
        label="Ambient Temp (°C)",
        initial=35,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        }),
        help_text="Enter temperature manually (e.g. 35)"
    )

    htl = forms.FloatField(
        label="HTL (L/2) Value",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter HTL value'
        }),
        help_text="Enter HTL value manually (e.g. 150.25)"
    )

    def clean_htl(self):
        htl = self.cleaned_data.get('htl')
        if htl < 150 or htl > 800:
            raise ValidationError("HTL must be between 150 and 800")
        return htl
