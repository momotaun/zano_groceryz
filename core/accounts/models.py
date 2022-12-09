
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set.')
        if not first_name:
            raise ValueError('The first name must be set.')
        if not last_name:
            raise ValueError('The last name must be set.')
        if not phone:
            raise ValueError('The Phone must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'Employee')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, first_name, last_name, phone, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    class UserTypes(models.TextChoices):
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        CUSTOMER = 'CUSTOMER', 'Customer'
        MEMBER = 'MEMBER', 'Member'

        
    
    email = models.EmailField(verbose_name=("E-mail"), unique=True, max_length=254)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    
    objects = CustomUserManager()
    
    first_name = models.CharField(verbose_name=("First name"), null=True, max_length=50)
    last_name = models.CharField(verbose_name=("Last name"), null=True, max_length=50)
    phone = models.CharField(verbose_name=("Phone number"), null=True, max_length=10)
    user_type = models.CharField(verbose_name=("User type"), max_length=50, choices=UserTypes.choices, default=UserTypes.CUSTOMER)
    
    
    
class EmployeeManager(CustomUserManager):
    def get_query(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=CustomUser.UserTypes.EMPLOYEE)
    
    
class MemberManager(CustomUserManager):
    def get_query(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=CustomUser.UserTypes.MEMBER)
    

class CustomerManager(CustomUserManager):
    def get_query(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=CustomUser.UserTypes.CUSTOMER)


class Employee(CustomUser):
    
    objects = EmployeeManager()
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = CustomUser.UserTypes.EMPLOYEE
        return super().save(*args, **kwargs)


class Member(CustomUser):
    
    objects = MemberManager()
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = CustomUser.UserTypes.MEMBER
        return super().save(*args, **kwargs)
    

class Customer(CustomUser):
    
    objects = CustomerManager()
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = CustomUser.UserTypes.CUSTOMER
        return super().save(*args, **kwargs)


class Profile(models.Model):

    class StokvelPeriod(models.TextChoices):
        NON_MEMBER = 'NON_MEMBER', 'Non Member'
        THREE_MONTHS = 'THREE_MONTHS', '3 Months'
        SIX_MONTHS = 'SIX_MONTHS', '6 Months'
        TWELVE_MONTHS = 'TWELVE_MONTHS', '12 Months'


    models.OneToOneField(Customer, verbose_name=("User"), on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    receive_newsletter = models.BooleanField(default=True)
    receive_promotions = models.BooleanField(default=True)
    istokvel_period = models.CharField(verbose_name=("iStokvel"), max_length=50, choices=StokvelPeriod.choices, default=StokvelPeriod.NON_MEMBER)