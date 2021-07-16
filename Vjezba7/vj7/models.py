from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.urls import reverse
# Create your models here.


class MyPersonManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email adress")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(email=self.normalize_email(email),
                        username=username)
        
        user.set_password(password) 
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username 
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Projection(models.Model):
    filmName = models.CharField(max_length=120) 
    duration = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '%s %s %s %s' % (self.filmName, self.duration, self.capacity, self.price)


class Person(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=50, unique=True)
    username = models.CharField(max_length=60, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USEARNAME_FIELD = 'email' 

    objects = MyPersonManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Ticket(models.Model):
    seatNumber = models.PositiveIntegerField(blank=False)
    projection = models.ForeignKey(Projection, on_delete=models.CASCADE) 
    user = models.ForeignKey(Person, related_name='projection_id', on_delete=models.CASCADE)  

    def __str__(self):
        return '%s %s %s' % (self.seatNumber, self.projection, self.user)
    
