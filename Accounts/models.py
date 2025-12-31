from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        # If username not supplied, default to email for compatibility
        username = username or email
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """
        Align with USERNAME_FIELD='email'. Django passes email/password, so make
        username optional and default it to email to avoid missing-arg errors.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        username = username or email
        return self.create_user(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=20, unique=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # REQUIRED FIELDS FOR ADMIN LOGIN
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    # LOGIN USING EMAIL
    USERNAME_FIELD = "email"
    # Prompt for employee_id when creating superuser to satisfy unique constraint
    REQUIRED_FIELDS = ["employee_id"]

    def _str_(self):
        return self.username

    # PERMISSIONS REQUIRED FOR DJANGO ADMIN
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/')

    def _str_(self):
        return f"Profile of {self.user.username}"
# Create your models here.