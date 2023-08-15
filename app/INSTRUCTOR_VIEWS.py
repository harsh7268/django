import requests
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.models import*
from django.contrib import messages
from app.EmployerEmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout


def INSTRUCTOR_Register(request):
    return render(request,'INSTRUCTOR/register.html')

def INSTRUCTOR_doregister (request):
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    username=request.POST.get("username")
    address=request.POST.get("address")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email,user_type=3)
        user.instructor.address=address
        user.save()
        messages.success(request,"Successfully Created Instructor")
        # return HttpResponse("success")
        return HttpResponseRedirect(reverse("instructor_login"))
    except:
        messages.error(request,"Failed to Create Instructor")
        
        return HttpResponseRedirect(reverse("INSTRUCTOR_Register"))


def dashboard(request):
    return render(request,'INSTRUCTOR/dashboard.html')

def add_course(request):

    if request.method == "POST":
        if request.method=="POST":
            course_name=request.POST.get('course_name')
            print(course_name)
        # course_pic=request.FILES.get('course_pic')
        # course_name = request.POST.get('course_name')
        # course_amt = request.POST.get('course_amt')
        # company_name = request.POST.get('company_name')
        # course_location = request.POST.get('course_location')
        # course_desc = request.POST.get('course_desc')
        # course_skills = request.POST.get('course_skills')
        # course_Experience = request.POST.get('course_Experience')


        # course = Course.objects.create(course_img=course_pic,course_name=course_name,course_amt=course_amt,company_name=company_name,course_location=course_location)
        # course.save()
        # messages.success(request,"Successfully Created Course")
    else:
        return render(request,'INSTRUCTOR/add_course.html')
        # messages.error(request,"Failed to Create Course")

    return render(request,'INSTRUCTOR/add_course.html')



def instructor_login(request):
    return render(request,'INSTRUCTOR/login.html')



def instructor_dologin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha Try Again")
            return HttpResponseRedirect(reverse("instructor_login"))
            # return HttpResponseRedirect("employer_login")

        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="3":
                return HttpResponseRedirect(reverse("instructor_dashboard"))
                # return HttpResponseRedirect('/admin_home')
            # elif user.user_type=="2":
            #     return HttpResponseRedirect(reverse("staff_home"))
            # elif user.user_type=="4":
            #    # return HttpResponse("MEMBERS PANEL")
            #     return HttpResponseRedirect(reverse("dashboard"))
            else:
                return HttpResponseRedirect(reverse("instructor_login"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("instructor_login")




def INSTRUCTOR_profile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # print(first_name)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("profile"))
            # redirect('/')
            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
    return render(request,'INSTRUCTOR/instructor_profile.html')