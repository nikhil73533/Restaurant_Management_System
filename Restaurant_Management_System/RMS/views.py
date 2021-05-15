from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render
from .models import Food,Review
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Avg, Count
from django.shortcuts import get_object_or_404
# Home page Backand Coding
def Home(request):
    return render(request,'Home.html')
 
# Reset Password functions
def reset_password(request):
    return render(request , 'user/Reset_Password.html')

#profile page Backand Coding
@login_required(login_url='/') 
def Profile(request):
    context = {}
    data = User.objects.get(id = request.user.id)
    context["data"] = data
    print("ok0")
    if(request.method == 'POST'):
        print("ok3")
        Name = request.POST['name']
        Email = request.POST['email']
        Address = request.POST['address']
        phone = request.POST['phone']
        user = User.objects.get(id = request.user.id)
        user.Name = Name
        user.email = Email
        user.Address = Address
        user.phone = phone
        user.save()

        if("profile" in request.FILES):
            img = request.FILES['profile']
            print(img)
            user.profile_pic = img
            user.save()
            print("ok1")
        context["status"] = "Changes Saved Successfully"
        return render(request,'profile_page.html',context)
        
    else:
       return render(request,'profile_page.html')

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
        return redirect('FoodMenu')
    else:
        return render(request, 'Food_Order.html',{'food': food}) 


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
        
        if(password==confirm_password):
            if(User.objects.filter(email=email).exists()):
                messages.info(request,'Email Taken')
                return render(request,'Login_Registration.html')
            elif(User.objects.filter(phone = phone_number).exists()):
                messages.info(request,'Phone Number Taken')
                return render(request,'Login_Registration.html')
            else:
                user  = User.objects.create_user(Name = Name,email = email,password = password,phone = phone_number,Address = address)
                user.save()
                return render(request,'Login_Registration.html')
        else:
            messages.info(request,'Password Does Not Match')
            return redirect('/')
    else:
        return render(request,'Login_Registration.html')


def Login(request):
    if(request.method=='POST'):
        password = request.POST['password']
        email  =  request.POST['email']
        user = auth.authenticate(request, email=email, password=password)
        if(user is not None):
            auth.login(request,user)
            return redirect('/',user= 'user')
        else:
            return render(request,'Login_Registration.html')
    else:
        return render(request,'Login_Registration.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')
    

# Food Manue
def FoodMenu(request):
    filter_bar = ""
    print(request.GET)
    food_type   = request.GET.get('ca ')
    print(food_type)
    if(food_type):
        print(food_type)
        food = Food.objects.filter(Food_Type = food_type)
       
        print(food)
    else:
        food = Food.objects.all()
    cate = []
    filter = Food.objects.all()
        
    for i in filter:
        cate.append(i.Food_Type)
    cate= set(cate)
    return render(request,'Food_menu.html',{'food':food,"cate":cate})

# Add To Cart
def Cart(request):
    return render(request,'Cart.html')

#Order Page
@login_required(login_url='Login') 
def FoodOrder(request,food_id):
    food = Food.objects.get(id = food_id)
    rating = Review.objects.filter(food_id = food_id)
    rate = Review.objects.filter(food_id= food_id).aggregate(Avg('rate'))
    num = Review.objects.filter(food_id= food_id).aggregate(Count('user'))
    print(rate["rate__avg"])
    print(num["user__count"])
    food.users = num["user__count"]
    food.Food_Avg_Rating = rate["rate__avg"]
    food.save()
    return render(request,'Food_Order.html',{"food":food,"rating":rating})



def Payment(request):
    return render(request,"Payment.html")


