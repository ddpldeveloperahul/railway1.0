from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from Accounts.forms import SignupForm, LoginForm,PasswordChangeForm,ProfileForm
from Accounts.models import Profile, CustomUser



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after signup go to login
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})



def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('railway')   # Redirect to other app
            else:
                messages.error(request, "Invalid email or password")

    return render(request, 'account/login.html', {"form": form})






def logout_view(request):
    logout(request)
    return redirect('login')

def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully!")
            # return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'account/changepassword.html', {'form': form})


@login_required(login_url='login')
def create_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        messages.error(request, "You already created a profile!")
        return redirect("profile")   # redirect to profile page

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # messages.success(request, "Profile created successfully")
            return redirect("profile")

    else:
        form = ProfileForm()

    return render(request, "account/profile_form.html", {"form": form})



@login_required(login_url='login')
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")   # send to create page

    return render(request, "account/profile2.html", {"profile": profile})
# def all_data_view(request):
#     detections = PulleyDetection.objects.all().order_by('-id')
#     return render(request, 'pulley_app/list_olddata.html', {'detections': detections})