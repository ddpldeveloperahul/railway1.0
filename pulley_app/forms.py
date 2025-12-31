from django import forms
from django.core.exceptions import ValidationError
from django import forms
 
CHART_TEMPERATURES = [10, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50]
CHART_HTL_VALUES = [200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800]
# obj =[150.1, 150.2, 150.3, 150.4, 150.5, 150.6, 150.7, 150.8, 150.9,150.10, 150.11, 150.12, 150.13, 150.14, 150.15, 150.16, 150.17, 150.18, 150.19,150.20, 150.21, 150.22, 150.23, 150.24, 150.25, 150.26, 150.27, 150.28, 150.29,150.30, 150.31, 150.32, 150.33, 150.34, 150.35, 150.36, 150.37, 150.38, 150.39,150.40, 150.41, 150.42, 150.43, 150.44, 150.45, 150.46, 150.47, 150.48, 150.49,150.50, 150.51, 150.52, 150.53, 150.54, 150.55, 150.56, 150.57, 150.58, 150.59,150.60, 150.61, 150.62, 150.63, 150.64, 150.65, 150.66, 150.67, 150.68, 150.69,150.70, 150.71, 150.72, 150.73, 150.74, 150.75, 150.76, 150.77, 150.78, 150.79,150.80, 150.81, 150.82, 150.83, 150.84, 150.85, 150.86, 150.87, 150.88, 150.89,150.90, 150.91, 150.92, 150.93, 150.94, 150.95, 150.96, 150.97, 150.98, 150.99,151.1, 151.2, 151.3, 151.4, 151.5, 151.6, 151.7, 151.8, 151.9,
# 151.10, 151.11, 151.12, 151.13, 151.14, 151.15, 151.16, 151.17, 151.18, 151.19,
# 151.20, 151.21, 151.22, 151.23, 151.24, 151.25, 151.26, 151.27, 151.28, 151.29,
# 151.30, 151.31, 151.32, 151.33, 151.34, 151.35, 151.36, 151.37, 151.38, 151.39,
# 151.40, 151.41, 151.42, 151.43, 151.44, 151.45, 151.46, 151.47, 151.48, 151.49,
# 151.50, 151.51, 151.52, 151.53, 151.54, 151.55, 151.56, 151.57, 151.58, 151.59,
# 151.60, 151.61, 151.62, 151.63, 151.64, 151.65, 151.66, 151.67, 151.68, 151.69,
# 151.70, 151.71, 151.72, 151.73, 151.74, 151.75, 151.76, 151.77, 151.78, 151.79,
# 151.80, 151.81, 151.82, 151.83, 151.84, 151.85, 151.86, 151.87, 151.88, 151.89,
# 151.90, 151.91, 151.92, 151.93, 151.94, 151.95, 151.96, 151.97, 151.98, 151.99
# ]

# CHART_HTL_VALUES = [
#     (round(i + j / 100, 2), f"{round(i + j / 100, 2)}")
#     for i in range(150, 751)
#     for j in range(1, 100)
# ]

TEMP_CHOICES = [(str(t), f"{t} °C") for t in CHART_TEMPERATURES]
HTL_CHOICES = [(str(v), f"{v} m") for v in CHART_HTL_VALUES]


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload Image")
    pole_name = forms.CharField(
        label="Pole Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the name/identifier of the pole (optional)"
    )
    # temperature = forms.ChoiceField(
    #     label="Ambient Temp (°C)",
    #     choices=TEMP_CHOICES,
    #     initial=str(35),
    #     widget=forms.Select(attrs={'class': 'form-select'}),
    #     help_text="Select a temperature value from the adjustment chart."
    # )
    temperature = forms.ChoiceField(
        label="Ambient Temp (°C)",
        choices=TEMP_CHOICES,
        initial=str(35),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Select a temperature value from the adjustment chart."
    )
    htl = forms.ChoiceField(
        label="HTL (L/2) Value",
        choices=HTL_CHOICES,
        initial=str(400),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select the HTL (L/2) value (200–800) from the chart."
    )
    # htl = forms.ChoiceField(
    #     label="HTL (L/2) Value",
    #     choices=CHART_HTL_VALUES,
    #     initial=str(400),
    #     widget=forms.TextInput(attrs={'class': 'form-select'}), 
    #     help_text="Select the HTL (L/2) value (150.1-750.99) from the chart."
    # )
    
    
class Upload_htl_temp(forms.Form):
    pole_name = forms.CharField(
        label="Pole Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the name/identifier of the pole (optional)"
    )
    # temperature = forms.ChoiceField(
    #     label="Ambient Temp (°C)",
    #     choices=TEMP_CHOICES,
    #     initial=str(35),
    #     widget=forms.Select(attrs={'class': 'form-select'}),
    #     help_text="Select a temperature value from the adjustment chart."
    # )
    temperature = forms.ChoiceField(
        label="Ambient Temp (°C)",
        choices=TEMP_CHOICES,
        initial=str(35),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Select a temperature value from the adjustment chart."
    )
    htl = forms.ChoiceField(
        label="HTL (L/2) Value",
        choices=HTL_CHOICES,
        initial=str(400),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select the HTL (L/2) value (200–800) from the chart."
    )
    
    
    

