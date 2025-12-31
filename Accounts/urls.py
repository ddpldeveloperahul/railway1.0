from django.urls import path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from . import views

urlpatterns = [
   
    path('profile/', views.profile_view, name='profile'),
    path('profile_form/', views.create_profile, name='profile_form'),
    
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('change-password/', views.change_password_view, name='change_password'),
    path('reset_password/', PasswordResetView.as_view(template_name="account/resetpassword.html"), name='reset_password'),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name="account/passwordrestdone.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="account/passwordconfirmation.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="account/passwordcomplete.html"), name='password_reset_complete'),  
  
]