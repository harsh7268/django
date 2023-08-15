import json
from django.shortcuts import redirect, render
import requests
import razorpay
from .models import*
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def home(request):
    course = Course.objects.all()
    job = Job.objects.all().order_by('id')[0:5]

    return render(request,'homepage/home.html',{'job':job,'course':course})

def joblisting(request):

    contact_list = Job.objects.all().order_by('-id')
    paginator = Paginator(contact_list, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print("page number",page_obj)
    # return render(request, 'list.html', {'page_obj': page_obj})
    return render(request,'homepage/job_listing.html',{'page_obj':page_obj})


def jobdetails(request,pk):
    
    job=Job.objects.all().filter(id=pk)

    return render(request,'homepage/job_details.html',{'job':job})

def course(request):
    course = Course.objects.all().order_by('-id')
    paginator = Paginator(course, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'homepage/course.html',{'course':page_obj})



def about(request):
     return render(request,'homepage/about.html')

def contact(request):
     return render(request,'homepage/contact.html')

def profile(request):
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
     return render(request,'homepage/profile.html')
     
@login_required(login_url='member_login')
def apply(request):
     return render(request,'homepage/apply.html')

def gallery(request):
    galary = gallary.objects.all()
    return render(request,'homepage/gallery.html',{'galary':galary})

def manage_gallery(request):
    galery = gallary.objects.all()
    return render(request,'HOD/manage_gallery.html',{'galery':galery})

def add_gallery(request):
    if request.method == "POST":
        galary = request.FILES.get('abb')
        galary_pic = gallary.objects.create(galary_pic=galary)
        galary_pic.save()
        messages.success(request,"Add Gallery Successfully")

    return render(request,'HOD/add_gallery.html')
def del_image(request,id):
    image=gallary.objects.get(id=id)
    image.delete()
    messages.success(request,"Photo has been deleted Successfully")
    return redirect('manage_gallery')
    


def show_galary(request):
    galery = gallary.objects.all()
    return render(request,'galary.html',{'galery':galery})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/EMPLOYERS/login2")
def success(request):
    return render(request,'success.html')


def worlker_list(request,id,bookingid):
    role = Role.objects.get(id=id)
    mem = Member.objects.filter(role_id = role)
    emp_gov=Employer.objects.get(admin=request.user.id)
    # monthly = Booking.objects.get(employer_id__admin = request.user.id)
    monthly = Booking.objects.get(id=bookingid)
    booking=Employer.objects.get(admin=request.user.id)
    count=monthly.no_of_worker
    monthly_offered=monthly.sallery_offerd
    depttype=emp_gov.section
    member = Member.objects.filter(Q(role_id_id=id) & Q(job_seeker=depttype))
    membercount=member.count()
    
    return render(request,'demo.html',{'member':member,'booking':booking,'mem':mem,'emp_gov':emp_gov,'count':count,'monthly_offered':monthly_offered,'membercount':int(membercount),'id':id,'bookingid':bookingid})   

@csrf_exempt
def booking_Success(request,bookingid):
        if request.method=="POST":
            order_id=request.POST.get("payment_id")
            user=Booking.objects.get(id=bookingid)
            user.payment_id=order_id
            user.paid=True
            temp=True
            user.save()
    # if request.method=="POST":
        # a=request.POST
        # # print(a)
        # order_id=""
        # temp=""
        # for key,val in a.items():
        #     if key=="razorpay_order_id":
        #         order_id = val
        #         break
        # booking = Employer.objects.get(admin=request.user.id)
        # booking_id=booking.id
        
        # user=Booking.objects.create(payment_id=order_id).first() 
        
        return render(request , 'employer/emp_success.html',{'checkuserPaid':temp,'bookingid':bookingid})   
def testing(request):
    event_list = Role.objects.all()
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        # print(id_list)
        event_list.update(is_employer=False)
        for x in id_list:
            Role.objects.filter(id= int(x)).update(is_employer=True)
    return render(request,'testing.html',{'event_list':event_list})