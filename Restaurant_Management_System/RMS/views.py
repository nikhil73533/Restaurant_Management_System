from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render


# Home page Backand Coding
def Home(request):
    return render(request,'Home.html')

#profile page Backand Coding
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
