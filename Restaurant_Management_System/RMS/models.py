from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.
class Food(models.Model):
    Food_Name = models.CharField(max_length = 100)
    Food_Price = models.IntegerField()
    Food_Avg_Rating = models.FloatField(null = True)
    Food_Type = models.CharField(max_length = 100)
    Description = models.CharField(max_length  = 5000)
    food_pic = models.ImageField(upload_to='Food/', blank = True, null = True)
    users = models.IntegerField(null = True)
    def __str__(self):
        return self.Food_Name

# Creating custom  user models here.
class MyUserManager(BaseUserManager):
    def profile_pic(self,profile_pic):
        user = self.model(
            profile_pic = profile_pic
        )
    def create_user(self,email,Name,phone,Address,password = None):
        if not email:
            raise ValueError("Email is required")
        if not Name:
            raise ValueError("Name is required")
        if not phone:
            raise ValueError("Please provide an active phone number")
        if not Address:
            raise ValueError("Please Provide Address")
        user = self.model(
            email = self.normalize_email(email),
            Name = Name,
            phone = phone,
            Address = Address
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,Name,phone,Address,password = None):
        user = self.create_user(
            email = email,
            Name = Name,
            phone = phone,
            password = password,
            Address  = Address,
        )
        user.is_admin = True
        user.is_staff =True
        user.is_superuser = True
        user.save(using = self._db)
        return user
       
class MyUser(AbstractBaseUser, PermissionsMixin): 
    Name = models.CharField(verbose_name = "Name",max_length = 50)
    email = models.EmailField(verbose_name = "email address",max_length = 60,unique = True,blank = True)
    Address = models.CharField(verbose_name = "Address",max_length = 200)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank = True, null = True)
    phone = models.CharField(max_length = 20,verbose_name = "phone number")
    last_login = models.DateTimeField(verbose_name = "last login",auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['Address','phone','Name']

    objects = MyUserManager()

    def __str__(self):
        return self.Name

    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True


# order model
class orders(models.Model):
    user_id = models.ForeignKey(MyUser,default=None,on_delete = models.CASCADE)
    food_id = models.ForeignKey(Food,default=None, on_delete = models.CASCADE)
    date_time = models.DateTimeField('date published')
    order_address = models.CharField(max_length=5000)
    quantity = models.IntegerField()
    deliver_status = models.BooleanField(default=False)

# FeedBack Model
class Review(models.Model):
    user = models.ForeignKey(MyUser,default=None,on_delete = models.DO_NOTHING)
    food = models.ForeignKey(Food,default=None, on_delete = models.DO_NOTHING)
    content = models.CharField(max_length=5000)
    rate = models.PositiveIntegerField()
    def __str__(self):
        return self.user.Name


    
