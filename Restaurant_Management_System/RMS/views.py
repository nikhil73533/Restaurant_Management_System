from django import template
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import math
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render
from .templatetags.cart import final_amount, discount_calculater,cart_count
from django.utils import timezone
from .models import Food,Review, orders, Bill,Booking,Table
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Avg, Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#Opening json file
with open("config.json","r") as p:
    parm = json.load(p)["parm"]

# Home page Backand Coding
def Home(request):
    return render(request,'Home.html')
 
# Reset Password functions
def reset_password(request):
    return render(request , 'user/Reset_Password.html',{"parm":parm})

#profile page Backand Coding
@login_required(login_url='/') 
def Profile(request):
    context = {}
    data = User.objects.get(id = request.user.id)
    context["data"] = data
    if(request.method == 'POST'):
        Name = request.POST['name']
        Email = request.POST['email']
        Address = request.POST['address']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        user = User.objects.get(id = request.user.id)
        user.Name = Name
        user.email = Email
        user.Address = Address
        user.phone = phone
        user.city = city
        user.state = state
        user.pincode = pincode
        user.save()

        if("profile" in request.FILES):
            img = request.FILES['profile']
            print(img)
            user.profile_pic = img
            user.save()
            print("ok1")
        messages.info(request,"Changes Saved Successfully")
        return render(request,'profile_page.html',context)
        
    else:
       return render(request,'profile_page.html',{"parm":parm})

# FeedBack
@login_required(login_url='/') 
def FeedBack(request,food_id):
    user = User.objects.get(id = request.user.id)
    food = Food.objects.get(id = food_id)
    if(request.method =='POST'):
        comment = request.POST['feedback']
        rating=  request.POST['rating']
        user_feedback = Review(user = user,food = food, content = comment, rate = rating)
        user_feedback.save()
        return redirect('FoodOrder',food_id = food_id)
    else:
        return redirect('FoodOrder',food_id = food_id)


#Registration and Login form 
User = get_user_model()
def Register(request):
    if(request.method == 'POST'):
        Name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        address  = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        
        if(password==confirm_password):
            if(User.objects.filter(email=email).exists()):
                messages.info(request,'Email Taken')
                return render(request,'Login_Registration.html')
            elif(User.objects.filter(phone = phone_number).exists()):
                messages.info(request,'Phone Number Taken')
                return render(request,'Login_Registration.html')
            else:
                user  = User.objects.create_user(Name = Name,email = email,password = password,phone = phone_number,Address = address,city = city,state = state,pincode = pincode)
                user.save()
                messages.add_message(request,messages.SUCCESS,'You have registered successfully')
                return render(request,'Login_Registration.html')
        else:
            messages.info(request,'Password Does Not Match')
            return redirect('/')
    else:
        return render(request,'Login_Registration.html',{"parm":parm})


def Login(request):
    if(request.method=='POST'):
        password = request.POST['password']
        email  =  request.POST['email']
        user = auth.authenticate(request, email=email, password=password)
        if(user is not None):
            auth.login(request,user)
            return redirect('/',user= 'user')
        else:
            messages.info(request,'Login Faild...')
            return render(request,'Login_Registration.html')
    else:
        return render(request,'Login_Registration.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')
    

# Food Menu
@login_required(login_url='Login')
def FoodMenu(request):
    user = User.objects.get(id = request.user.id)
    ord = orders.objects.filter(user = user)
    ord = list(ord)
    qty = 0
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    filter_bar = ""
    food_type   = request.GET.get('ca ')
    if(food_type):
        food = Food.objects.filter(Food_Type = food_type)
    else:
        food = Food.objects.all()
    cate = []
    filter = Food.objects.all()
        
    for i in filter:
        cate.append(i.Food_Type)
    cate= set(cate)
    if(request.method =='POST'):
        search = request.POST["box"]
        food = Food.objects.filter(Q(Food_Name__icontains=search))
        filter = Food.objects.all()
        cate = []
        for i in filter:
            cate.append(i.Food_Type)
        cate= set(cate)
    return render(request,'Food_menu.html',{'food':food,"cate":cate,"qty":qty,"ord":ord,"parm": parm})

# Add To Cart
@login_required(login_url='Login') 
def Cart(request):
    if(request.method=="POST"):
        food = request.POST['food_id']
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(food)
            if(quantity):
                if(remove):
                    if(quantity<=1):
                        cart.pop(food)
                    else:
                        cart[food] = quantity - 1
                else:
                    cart[food] = quantity + 1
            else:
                cart[food] = 1
        else:
            cart = {}
            cart[food] = 1
        request.session['cart'] = cart
    return redirect('FoodMenu')



@login_required(login_url='Login')     
def AddCart(request):
    ids = list(request.session.get('cart'))
    product = Food.objects.filter(id__in = ids)
    user = User.objects.get(id = request.user.id)
    odr = orders.objects.filter(user = user)
    
    SGST = 5
    CGST  = 5
    penilty = user.penilty
    cart = request.session.get('cart')
    lis = [SGST,CGST,penilty,cart,product]
    if(request.method=='POST'):
        Address = request.POST.get('Address')
        City = request.POST.get('city')
        State = request.POST.get('state')
        Pincode = request.POST.get('pincode')
        payment_method = request.POST.get('paymentmethod')
        if(payment_method=='COD'):
            print("ok")
            print(product)
            count = 0
            for p in product:
                discount_amount = discount_calculater(p,cart)
                Amount = final_amount(lis,p)
                qty = cart_count(p,cart)
                ord = orders(user = user,food = p,date_time = timezone.now(),state = State,city = City,order_address = Address,pincode = Pincode,quantity =qty ,deliver_status = False,total_amount =Amount )
                ord.save()
                bill = Bill(order_no = ord,user = user,food = p,payment_status =False,discount = discount_amount,tex = 10,penilty = penilty,total_amount = Amount)
                bill.save()
                count+=1
            success(request)
            messages.add_message(request,messages.SUCCESS,'Your Order have done successfully!')
            request.session['cart'] = {}
            user.penilty = 0
            user.save()
            
            return redirect('AddCart')
    return  render(request,'cart_product.html',{'product':product,"order":odr, "user":user,'TEX':CGST + SGST,"lis":lis,"parm":parm})

#Order Page
@login_required(login_url='Login') 
def FoodOrder(request,food_id):
    discount = False
    food = Food.objects.get(id = food_id)
    new_food_price = food.Food_Price
    user = User.objects.get(id = request.user.id)
    ord = orders.objects.filter(user = user)
    ord = list(ord)
    if(food.Discount_In_Percentage>0):
        discount = True
        difference = (food.Food_Price)*((food.Discount_In_Percentage)/(100))
        new_food_price = int(food.Food_Price - difference)

    qty = 1
    if(request.method =='POST'):
        value = request.POST['qty']
        remove = request.POST.get('remove')
        value = int(value)
        if(qty>0):
            if(remove):
                qty = value-1
            else:
                qty = value + 1
        else:
            qty = 1

    rating = Review.objects.filter(food_id = food_id)
    rate = Review.objects.filter(food_id= food_id).aggregate(Avg('rate'))
    num = Review.objects.filter(food_id= food_id).aggregate(Count('user'))
    print(rate["rate__avg"])
    print(num["user__count"])
    food.users = num["user__count"]
    food.Food_Avg_Rating = rate["rate__avg"]
    food.save()
    return render(request,'Food_Order.html',{"food":food,"rating":rating,"Discount":discount,"new_food_price":new_food_price,"qty":qty,"ord":ord,"parm":parm})



@login_required(login_url='Login') 
def Payment(request,food_id,qty ):
    food = Food.objects.get(id = food_id)
    user = User.objects.get(id = request.user.id)
    discount = False
    difference =0
    penilty = user.penilty
    CGST = 5
    SGST = 5
    new_food_price = food.Food_Price
    # Adding Discount
    if(food.Discount_In_Percentage>0):
        discount = True
        difference = (food.Food_Price)*((food.Discount_In_Percentage)/(100))
        new_food_price = (food.Food_Price - difference)
    
    Total_price = round(new_food_price * int(qty),4)
    # Final price
    print(penilty)
    Final_price = round(Total_price + 0 + Total_price*(CGST*0.01) + Total_price*(SGST*0.01),4)
    if(penilty):
        Final_price = round(Total_price + penilty + Total_price*(CGST*0.01) + Total_price*(SGST*0.01),4)
   
    message = ""
    #Order count 
    odr = orders.objects.filter(user = user)
    if request.method == 'POST':
        Address = request.POST.get('Address')
        City = request.POST.get('city')
        State = request.POST.get('state')
        Pincode = request.POST.get('pincode')
        payment_method = request.POST.get('paymentmethod')
        if(payment_method == "COD"):
                ord = orders(user = user,food = food,date_time = timezone.now(),order_address = Address,state = State,city = City,pincode = Pincode,quantity = qty,deliver_status = False,total_amount = Final_price)
                ord.save()
                bill = Bill(order_no =ord,user = user,food  = food,payment_status = False,discount = difference,tex = 10, penilty = penilty,total_amount = Final_price)
                bill.save()
                user.penilty = 0
                user.save()
                messages.add_message(request,messages.SUCCESS,'Your Order have done successfully!')
                success(request)
        elif(payment_method =="UPI" or payment_method =="CARD"):
            messages.info(request,"This service is not avaible now")

    return render(request,"Payment.html", {"user":user,"food":food,"Discount":discount,"difference":difference,"new_food_price":new_food_price,"qty":qty,"Total_price":Total_price,"final_price":Final_price,"user":user,'odr':odr,'CGST':CGST,'SGST':SGST,"parm":parm})

#MyOrders Page
@login_required(login_url='Login')
def MyOrders(request):
    user = User.objects.get(id = request.user.id)
    order = orders.objects.filter(user_id =user).order_by('-date_time')
    bills = Bill.objects.filter(user = user)
    count = 0
    lis = [request.session.get('cart')]
    if(request.method == 'POST'):
        count+=1
        if(request.POST.get('cancle')):
                print("ok")
                oddr = request.POST.get('order_no')
                odr = orders.objects.get(id = oddr)
                print(odr)
                print(odr.total_amount)
                if(count<2):
                    print("first")
                    user.penilty = math.ceil((odr.total_amount)*0.1)
                else:
                    print("second")
                    user.penilty = user.penilty + math.ceil((odr.total_amount)*0.2)
                print(user.penilty)
                user.save()
                odr.delete()
                messages.add_message(request,messages.SUCCESS,'Your Order have cancled successfully!')

        else:
                print("okkk2")
                oddr = request.POST.get('order_no')
                odr = orders.objects.get(id = oddr)
                odr.delete()
                messages.add_message(request,messages.SUCCESS,'Your Order have cancled successfully!')
    return render(request,'MyOrders.html',{'user':user,"parm":parm,'orders':order,"bills":bills})

# Sending Conformation email
def success(request):
    user = User.objects.get(id = request.user.id)
    template = render_to_string('email_templates.html',{'user':user})
    print("started")
    email  = EmailMessage(
        'Thanks for purhcasing the food',
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    print("progress")
    email.fail_silently = False
    email.send()

# Handeling Time  and penilties
def HandelBooking(capicity):
    Capicity = Table.objects.filter(capicity = capicity)

# Contact page
def Contact(request):
    return render(request,'index.html',{"parm":parm})


# Boking Table
def BookTable(request):
    print("ok")
    if(request.method=='POST'):
        Date = request.POST.get("Date")
        Time = request.POST.get("Time")
        Members = request.POST.get("members")
        date_time = Date + " " + Time
        date_object = datetime.strptime(date_time,"%Y-%m-%d %H:%M")
        if(timezone.now()>date_object):
            messages.info(request,"Invlid Input")
            HandelBooking(Members)
            return redirect('BookTable')
        
        Boking = Booking(No_Of_Memebers = Members,Time_Date = date_object)
        Boking.save()
        messages.info(request,"Successfully Booked")
    return render(request,'Book_Table.html',{"parm":parm})

