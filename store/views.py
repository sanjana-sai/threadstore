from django.shortcuts import render,redirect

from store.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from store.models import Product,Basket,BasketItems,Size,Order

# Create your views here.

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

           # data=form_instance.cleaned_data

            #User.objects.create_user(**data)

            print("account created")

            return redirect("register")

        return render(request,"register.html",{"form":form_instance})


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            password=data.get("password")

            user_object=authenticate(request,username=uname,password=password)
            
            print(user_object)

            if user_object:

                login(request,user_object)

                print("session started")

            return redirect("index")
        
        print("login failed")

        return render(request,"login.html",{"form":form_instance})



class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()
        
        return render(request,"index.html",{"data":qs})


class ProductDetailsView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"details.html",{"data":qs})

    
#url:localhost:product/{id}/carts/add/

class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        #basket_obj=Basket.objects.get(owner=request.user)

        basket_obj=request.user.cart    # using related name


        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)

        qty=request.POST.get("qty")

        print(product_obj,size_name,qty)

        basketobj_item=BasketItems.objects.filter(basket_object=basket_obj,product_object=product_obj,size_object=size_obj,is_order_placed=False)

        if basketobj_item :

            basketobj_item[0].quantity+=int(qty)

            basketobj_item[0].save()

        else:

            BasketItems.objects.create(
            basket_object=basket_obj,
            product_object=product_obj,
            size_object=size_obj,
            quantity=qty
        )




        
            print("items added to cart")



        return redirect("index")


class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False).order_by("-created_date")  # using related name

        # (or)

        # basket_obj=Basket.objects.get(owner=request.user)

        # qs=BasketItems.objects.filter(basket_object=basket_obj,is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})
    
#url:lo/basketitem/{id}/remove/

class CartItemDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItems.objects.get(id=id).delete()

        return redirect("cart-summary")


class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    


class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):


        action =request.POST.get("action")  #increement or decrement

        id=kwargs.get("pk")

        basketitem_object=BasketItems.objects.get(id=id)

        if action == "increment" :

            basketitem_object.quantity+=1
        else:

            basketitem_object.quantity-=1

        basketitem_object.save()


        return redirect("cart-summary")


class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    

    def post(self,request,*args,**kwargs):

        #print(request.POST)

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment mode")
        
        print(email,phone,address,pin,payment_mode)

        user_obj=request.user

        basket_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)

        if payment_mode == "cod":

            order_obj=Order.objects.create(
                                
                        user_object=user_obj,

                        delivery_address=address,
                        phone=phone,
                        email=email,
                        pin=pin,
                        payment_method=payment_mode,

            )
        for bi in basket_item_objects:

            order_obj.basket_item_object.add(bi)

            bi.is_order_placed=True

            bi.save()

        order_obj.save()    

        return redirect("index")

class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")
        
        return render(request,"order_summary.html",{"data":qs})
    





        