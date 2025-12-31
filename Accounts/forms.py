from django import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from Accounts.models import CustomUser,Profile
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        label="Email"
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        label="Username"
    )

    employee_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employee ID'}),
        label="Employee ID"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'employee_id', 'password']  # confirm_password is not a model field

    # 🔥 Validate Email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email

    # 🔥 Validate Employee ID
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if CustomUser.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("Employee ID already exists!")
        return employee_id

    # 🔥 Validate Password Match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match!")

        return cleaned_data

    # 🔥 Save user with hashed password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password

        if commit:
            user.save()
        return user

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter password',
#         })
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Confirm password',
#         })
#     )

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'employee_id', 'password', 'confirm_password']

#         # ✅ Widgets must be defined inside Meta
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter full name',
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter email address',
#             }),
#             'employee_id': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter employee ID',
#             }),
#         }

#     # ✅ Password validation logic
#     # 
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if CustomUser.objects.filter(username=username).exists():
#             raise ValidationError("This username is already taken.")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if CustomUser.objects.filter(email=email).exists():
#             raise ValidationError("This email is already registered.")
#         return email

#     def clean_employee_id(self):
#         employee_id = self.cleaned_data['employee_id']
#         if CustomUser.objects.filter(employee_id=employee_id).exists():
#             raise ValidationError("This employee ID is already in use.")
#         return employee_id

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             raise ValidationError("Password and Confirm Password do not match.")
        
# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)


# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter email',
#         }),
#         label="Email:"
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter password',
#         }),
#         label="Password:"
#     )
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class passwordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter old password',
        }),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
        }),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        }),
        label="Confirm New Password"
    )

    
class ProfileForm(forms.ModelForm):
    # user = forms.EmailField(widget=forms.Select(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control fw-bold'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control fw-bold'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.Select(attrs={'class': 'form-control fw-bold'}))

    class Meta:
        model = Profile
        fields = ['user', 'mobile_number', 'address', 'profile_photo']
        
    def clean_user(self):
        user = self.cleaned_data['user']
        if Profile.objects.filter(user=user).exists():
            raise forms.ValidationError("This user already has a profile.")
        return user
        
        
        