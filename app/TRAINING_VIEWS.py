import requests
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.models import*
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from app.EmailBackEnd import EmailBackEnd




def TRAINING_Register(request):
    role = Role.objects.all()
    return render(request,'TRAINING/register.html',{'role':role})



def do_training_register(request):
   if request.method == "POST":

      role_id = request.POST.get("role")
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      father_name = request.POST.get("father_name")
      gender = request.POST.get("gender")
      mobile_no = request.POST.get("mobile_no")
      dob = request.POST.get("dob")
      adhaar = request.POST.get("adhaar")
      pan_no = request.POST.get("pan_no")
      caste = request.POST.get("caste")
      city = request.POST.get("city")
      state = request.POST.get("state")
      pin = request.POST.get("pin")
      address = request.POST.get("address")
      email = request.POST.get("email")
      
      password = "123456"
      

      role=Role.objects.get(id=role_id)

      amount = int(request.POST.get("amount"))*100 
    #   client=razorpay.Client(auth =("rzp_test_czVP739sBN5blU" , "MBpgYsg92tAkraZtv5BMyLeq"))
      
    #   payment=client.order.create({'amount':amount, 'currency':'INR' , 'payment_capture' : '1'})
      user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,adhaar=adhaar,password=password,user_type=5)
      user.training.father_name=father_name
      user.training.gender=gender
      user.training.mobile_no=mobile_no
      user.training.dob=dob
      # user.member.adhaar=adhaar
      user.training.pan_no=pan_no
      user.training.caste=caste
      user.training.city=city
      user.training.state=state
      user.training.pin=pin
      # user.member.email=email
      user.training.address=address

      user.training.role_id=role

      user.training.amount=amount
    #   user.training.payment_id=payment['id']
      user.save()
      context = {
         'fname':fname,
         'lname':lname,
         'username':username,
         'email':email,
        #  'payment':payment

      }

      
      # coffee=Coffee(name = name , amount = amount , payment_id = payment['id'])
      # coffee.save()
      return render(request , 'TRAINING/do_training_register.html',context)

@csrf_exempt
def Success(request):
 if request.method=="POST":
     a=request.POST
     print(a)
     order_id=""
     for key,val in a.items():
      if key=="razorpay_order_id":
        order_id = val
        break
     user=Training.objects.filter(payment_id=order_id).first() 
     user.paid=True
     user.save()
 return render(request , 'TRAINING/success.html')   


def TRAINING_login(request):
    return render(request,'TRAINING/login.html')


def training_doLogin(request):
    
        user=EmailBackEnd.authenticate(request,username=request.POST.get("adhaar"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="5":
                return HttpResponseRedirect(reverse("training_dashboard"))
             
        else:
            messages.error(request,"Invalid adhaar number or password !!")
            return HttpResponseRedirect(reverse("TRAINING_login"))

@login_required(login_url='TRAINING_login')
def dashboard(request):
    return render(request,'TRAINING/dashboard.html')
    
@login_required(login_url='TRAINING_login')
def TRAINING_process(request):
    return render(request,'TRAINING/process.html')

def training_payment_information(request):
    training = Training.objects.filter(admin=request.user)

    return render(request,'TRAINING/payment_info.html',{'training':training})
