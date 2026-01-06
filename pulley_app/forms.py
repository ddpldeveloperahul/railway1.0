from django import forms
from django.core.exceptions import ValidationError

regulating_type_choices = [
    ('3 PULLEY (MODIFIED)', '3 PULLEY (MODIFIED)'),
    ('3 PULLEY (SMALL)', '3 PULLEY (SMALL)'),
    ('3 PULLEY TYPE', '3 PULLEY TYPE'),
    ('5 PULLEY TYPE', '5 PULLEY TYPE'),
]

station_choices = [
    ('HG-WD', 'HG-WD'),
    ('NGS', 'NGS'),
    ('BOT', 'BOT'),
    ('GDGN', 'GDGN'),
    ('GUR', 'GUR'),
    ('SVG', 'SVG'),
]

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload Image")

    pole_name = forms.CharField(
        label="Pole Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    regulating_type = forms.ChoiceField(
        label="Regulating Type",
        choices=regulating_type_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    station = forms.ChoiceField(
        label="Station",
        choices=station_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    temperature = forms.FloatField(
        label="Ambient Temp (°C)",
        initial=35,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        }),
        # help_text="Enter ambient temperature in Celsius"
    )

    htl = forms.FloatField(
        label="HTL (L/2) Value",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter HTL value'
        }),
        # help_text="Enter HTL value manually (e.g. 150.25)"
    )
    latitude = forms.FloatField(
        label="Latitude",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.000001',
            'placeholder': 'Enter latitude'
        }),
    )
    longitude = forms.FloatField(
        label="Longitude",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.000001',
            'placeholder': 'Enter Longitude'
        }),
    )
    
  

    def clean_htl(self):
        htl = self.cleaned_data.get('htl')
        if htl < 150 or htl > 800:
            raise ValidationError("HTL must be between 150 and 800")
        return htl


class Upload_htl_temp(forms.Form):
    pole_name = forms.CharField(
        label="Pole Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the name/identifier of the pole (optional)"
    )

    temperature = forms.FloatField(
        label="Ambient Temp (°C)",
        min_value=10,
        max_value=50,
        initial=35.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'e.g. 35'
        }),
        help_text="Enter ambient temperature in Celsius"
    )

    htl = forms.FloatField(
        label="HTL (L/2) Value",
        min_value=150,
        max_value=800,
        initial=400,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '1',
            'placeholder': '150 – 800'
        }),
        help_text="Enter HTL (L/2) value (150–800)"
    )
    def clean_htl(self):
        htl = self.cleaned_data.get('htl')
        if htl < 150 or htl > 800:
            raise ValidationError("HTL must be between 150 and 800")
        return htl