from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save


# Create your models here.

class Size(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    
    def __str__(self):

        return self.name
    


class Brand(models.Model):
    
    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    
    def __str__(self):

        return self.name

class Category(models.Model):


    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    
    def __str__(self):

        return self.name
    
class Tag(models.Model):

    name=models.CharField(max_length=200,unique=True)

   
    def __str__(self):

        return self.name



class Product(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField(null=True,blank=True)

    price=models.PositiveIntegerField()

    image=models.ImageField(upload_to="productimages",null=True,default="product_images/default.jpg")

    size_object=models.ManyToManyField(Size)

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    tag_object=models.ManyToManyField(Tag)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    
    def __str__(self):

        return self.title
    

class Basket(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    
    def __str__(self):

        return self.owner.username
    
    @property
    def cart_item_count(self):

        return self.cartitems.filter(is_order_placed=False).count()
    
    @property
    def cart_total(self):

      basket_items=self.cartitems.filter(is_order_placed=False)  

      total_price=0

      for bi in basket_items:
          
        total_price+=bi.total_amount

      return total_price

    
class BasketItems(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitems")

    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    is_order_placed=models.BooleanField(default=False)

    @property
    def total_amount(self):

        return self.product_object.price * self.quantity


class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="myorders")

    basket_item_object=models.ManyToManyField(BasketItems)

    phone=models.CharField(max_length=200)

    pin=models.CharField(max_length=200,null=True)

    email=models.EmailField()

    delivery_address=models.CharField(max_length=200)

    excepted_delivery_date=models.DateField(null=True)

    pay_options=(
        ("cod","cod"),
        ("online","online"),
        
    )

    payment_method=models.CharField(max_length=200,choices=pay_options,default="cod")

    order_id=models.CharField(max_length=200,null=True)   #null is given for database 

    is_paid=models.BooleanField(default=False)

    order_status=(
        ("order_confirmed","order_confirmed"),
        ("dispatched","dispatched"),
        ("in_transit","in_transit"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),

    )

    status=models.CharField(max_length=200,choices=order_status,default='order_confirmed')

    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    

def create_basket(sender,instance,created,**kwargs):

    if created:

        Basket.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)
    









