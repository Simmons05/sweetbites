from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser,UserManager,PermissionsMixin
from datetime import datetime,date
from django.utils import timezone

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self,email=None,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password,** extra_fields)
    
    def create_superuser(self,email=None,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self._create_user(email,password,** extra_fields)
    
class CustomUser(AbstractUser):
    email=models.EmailField(blank=True,default="",unique=True)
    name=models.CharField(max_length=100,default="",blank=True)
    phone=models.CharField(max_length=12)
    
    
    
    date_joined=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(blank=True,null=True)
    
    objects=CustomUserManager()
    
    USERNAME_FIELD="email"
    EMAIL_FIELD="email"
    REQUIRED_FIELDS=[]
    
    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split("@")[0]

class Motel(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user")
    room_id=models.CharField(max_length=100)
    room_photo=models.ImageField(upload_to='media/')
    room_price=models.DecimalField(max_digits=10,decimal_places=2)
    room_cid=models.DateField(auto_now_add=True)
    room_cod=models.DateField()
    is_booked=models.BooleanField(default=False)
    room_bill=models.DecimalField(max_digits=10,decimal_places=2)
    
class Restaurant(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    food_id=models.CharField(max_length=100)
    food_photo=models.ImageField(upload_to='media/',default="static/food/Tortilla.jpg")
    food_quantity=models.IntegerField()
    food_price=models.DecimalField(max_digits=10,decimal_places=2)
    food_bill=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Food: {self.food_id}| {self.food_price}"
    
    def save(self,*args,**kwargs):
        self.my_dish=self.user.name+self.food_id+str(self.food_photo)+self.food_price+(self.food_quantity*self.food_price)
        super(Restaurant,self).save(*args,**kwargs)


class Bar(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    drink_id=models.CharField(max_length=100)
    drink_photo=models.ImageField(upload_to='media/')
    drink_quantity=models.IntegerField()
    drink_price=models.DecimalField(max_digits=10,decimal_places=2)
    drink_bill=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"Drink: {self.drink_id} | {self.drink_price}"
    
    def save(self,*args,**kwargs):
        self.my_drinks=self.user.username+self.drink_id+self.drink_photo+"Kes "+str(self.drink_price)+"Kes "+str((self.drink_quantity*self.drink_price))
        super(Bar,self).save(*args,**kwargs)


class DrinksStockOrder(models.Model):
    #id=models.AutoField(primary_key=True)
    order_name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order_qty=models.PositiveIntegerField(default=1)
    total_bill=models.DecimalField(max_digits=10,decimal_places=2)
    
#user orders a room
class OrderRoom(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    room=models.ForeignKey(Motel,on_delete=models.CASCADE)
    room_price=models.DecimalField(max_digits=10,decimal_places=2)
    check_in_date=models.DateField(auto_now_add=True)
    check_out_date=models.DateField()

    def __str__(self):
        return f"Room {self.room.room_id}|{self.check_in_date} to {self.check_out_date}"

    def save(self,*args,**kwargs):
        self.my_room=self.user.name+self.room.room_id+str(self.check_in_date)+str(self.check_out_date)
        super(OrderRoom,self).save(*args,**kwargs)

    
#user orders food and drinks
class OrderFood(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    food=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    bill=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    

    def __str__(self):
        return f"Ordered: {self.quantity} - {self.food.food_id}"

    def save(self,*args,**kwargs):
        self.my_order=self.user.name+self.food.food_id+str(self.quantity)
        super(OrderFood,self).save(*args,**kwargs)
    
class OrderDrinks(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    drink=models.ForeignKey(Bar,on_delete=models.CASCADE)

    def __str__(self):
        return f"Ordered:{self.drink.drink_id}|{self.drink.drink_price}"

    def save(self,*args,**kwargs):
        self.my_drinks=self.user.name+self.drink.drinks_id+str(self.drink.drink_quantity)+str(self.drink.drink_price)
        super(OrderDrinks,self).save(*args,**kwargs)

'''
#update total bill in DrinksStockOrder when orders are placed
class AllOrders(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    room_order=models.ForeignKey(OrderRoom,on_delete=models.CASCADE,null=True)
    room_order_price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    foods_order=models.ForeignKey(OrderFood,on_delete=models.CASCADE,null=True)
    foods_order_price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    drinks_order=models.ForeignKey(OrderDrinks,on_delete=models.CASCADE,null=True,default=0)
    drinks_order_price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    room_order_bill=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    foods_order_bill=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    phone=models.CharField(max_length=12,default='',null=True)
    is_completed=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order for Room: {self.room_order.room.room_id}"
    
    def save(self,*args,**kwargs):
        #self.all_items=self.foods_order.food.food_id+""+self.room_order.room.room_id
        self.total_bill=int(self.room_order_bill)+int(self.foods_order_bill)
        super(AllOrders,self).save(*args,**kwargs)'''