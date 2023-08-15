import requests
import json
from django.shortcuts import redirect, render
import json
from .models import*
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from io import BytesIO
def dummy(request):
    city = City.objects.all()
    role = Role.objects.all()
    return render(request,'dummy.html',{'city':city,'role':role})

def register(request):
    
    demo3 = ""
    city_search=""
    city_name = ""
    role = Role.objects.all()
    city = City.objects.all()
    if request.method == "POST":
        role3 = request.POST.get('testing')
        city_search = request.POST.get('city_search')
        cityy = City.objects.get(id=role3)
        role2 = Role.objects.filter(city_id=cityy)
        demo3 = role2
        city_name = City.objects.get(id=city_search)
        
        
    return render(request,'MEMBERS/register.html',{'role':role,'city':city,'demo':demo3,'city_name':city_name})

def instant_service(request):
    response = requests.get('https://api.onit.services/admin/get-all-services')
    data = response.json()
    return render(request, 'MEMBERS/instantservice.html', {'data': data})

def technicianlist(request):
    response = requests.get('https://api.onit.services/admin/get-all-technician')
    data = response.json()
    if request.method == 'POST':
        servicesRequired = request.POST.get('services')
        specificRequirement = request.POST.get('specificReq')
        name = request.POST.get('name')
        phoneNumber = request.POST.get('phoneNumber')
        alternativePhoneNumber = request.POST.get('alternativePhn')
        houseNumber = request.POST.get('houseNumber')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        timePreferences = request.POST.get('pref')
        offerCode = request.POST.get('offerCode')
        if phoneNumber==alternativePhoneNumber:
            messages.error(request,"Phone Number and alternative Phone Number cannot be same")
            return redirect('register')
        context = {
            "personal_details":
            {
                "primary_phone":
                {
                    "country_code": "+91",
                    "mobile_number": phoneNumber
                },
                "name": name
            },
            "specific_requirement": specificRequirement,
            "service_provided_for": servicesRequired,
            "address_details":
            {
                "house_number": houseNumber,
                "locality": locality,
                "city": city,
                "state": state,
                "pincode": pincode,
                "country": country
            },

            "offers_applied":
            {
                "offer_code": offerCode
            },

                "center_obj_id": "63b9b0a18557944e0d37a01a",
                 "time_preference":{
                "time_preference_type":timePreferences,
                "specific_date_time": "2023-01-21T05:07:00.719Z"
            }
        }
        response = requests.post(
            'https://api.onit.services/center/public-ticket-booking', json=context)

    return render(request,'MEMBERS/techlist.html',{'data':data,'pincode':pincode,'serviceOffered':servicesRequired})

def technician_detail(request,id):
    response = requests.get('https://api.onit.services/admin/get-all-technician')
    data = response.json()
    filtered_data = [item for item in data['data'] if item['_id'] == id]
    return render(request,'MEMBERS/techdetail.html',{'data':filtered_data})



def douserregister(request):
    if request.method == "POST":

    
        role_id = request.POST.get("role_id")
        role_id2 = request.POST.get("role_id2")

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
        marital_status = request.POST.get("marital_status")
        job_seeker = request.POST.get("job_seeker")
        adhar_front = request.FILES.get('adhar_front')
        adhar_back = request.FILES.get('adhar_back')
        password = request.POST.get('mobile_no')
        role=Role.objects.get(id=role_id)
        amount = int(request.POST.get("amount"))*100 
        # client=razorpay.Client(auth =("rzp_test_czVP739sBN5blU" , "MBpgYsg92tAkraZtv5BMyLeq"))
        
        # payment=client.order.create({'amount':amount, 'currency':'INR' , 'payment_capture' : '1'})
        user=CustomUser.objects.create_user(username=username,adhaar=adhaar,password=password,user_type=4)
        user.member.father_name=father_name
        user.member.gender=gender
        user.member.mobile_no=mobile_no
        user.member.dob=dob
        user.member.adhaar=adhaar
        user.member.pan_no=pan_no
        user.member.caste=caste
        user.member.city=city
        user.member.state=state
        user.member.pin=pin
        user.member.marital_status=marital_status
        user.member.job_seeker=job_seeker
        # user.member.email=email
        user.member.address=address
        user.member.adhar_front=adhar_front
        user.member.adhar_back=adhar_back

        user.member.role_id=role
        
        user.member.amount=amount/100
        # user.member.payment_id=payment['id']
        # if user.member.paid == True:
        user.save()
        
        

    #   
        context = {
            
        'username':username,
        # 'father_name':father_name,
        'mobile_no':mobile_no,
        'adhaar':adhaar,     
        # 'payment':payment,
        'dob':dob,
        'adminid':user.member.admin_id,
        }

        return render(request , 'homepage/doregister.html',context)
    return render(request,'homepage/doregister.html')
      
        
def member_qr(request,adminid):
    return render(request,'MEMBERS/member_qr.html',{'adminid':adminid})


def emp_booked(request,empid,status):
    memid=Member.objects.get(admin=request.user.id).id
    mem=Member.objects.get(admin=request.user.id)
    member=Notification.objects.get(Q(emp_id=empid) & Q(mem_id=memid))
    emp=Employer.objects.get(id=empid)
    othermem=Notification.objects.filter(mem_id=memid).exclude(emp_id=empid)
    if status == 'True':
        member.status='Accepted'
        mem.is_employed=True
        mem.save()
        member.save()
        for i in othermem:
          i.status='Rejected'
          i.save()
    else:
        member.status='Rejected'
        member.save()
    return render(request,'MEMBERS/emp_booked.html',{'member':member,'status':status,'employer':emp})



class GeneratePDF(View):
    def get(self, request):
        # Get registration details from the database or form submission data
        # ...
        admin_id = request.GET.get('admin_id')
        print(admin_id)
        mem=Member.objects.get(admin=admin_id)
        registration_details = {
            'name': mem.admin,
            'email': 'info@clc.com',
            'phone': mem.mobile_no,
            'address': mem.address,
            'registration_date': mem.created_at.strftime('%b %d, %Y')
        }

        # Render the PDF template with registration details as context variables
        template = get_template('MEMBERS/registration_pdf.html')
        context = {'registration_details': registration_details}
        html = template.render(context)

        # Create a PDF response object with appropriate headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="registration.pdf"'

        # Generate PDF file and write to response
        pisa.CreatePDF(html, dest=response)

        return response

def qr_status(request,adminid):
    if request.method=="POST":
        # try:
            # Made an HTTP request to the URL that sends the text message
            # response = requests.get('http://world.masssms.tk/V2/http-api.php?apikey=pok9POX1PAImVeyq&senderid=ONITad&peid=1501465370000036089&templateid=1507164369557408315&senderid=ONITad&number=917838716761&message=Use OTP 9841 to login to your OniT account.&format=json url')
            payment_id=request.POST.get("payment_id")
            mem=Member.objects.get(admin_id=adminid)   
            mem.payment_id=payment_id
            mem.save()
            pdf_url = reverse('generate_pdf')
        # except requests.exceptions.RequestException as e:
        #     # Handle any exceptions that occurred during the request
        #     return HttpResponse('Error occurred: {}'.format(str(e)))

       
    return render(request,'MEMBERS/qr_status.html',{'pdf_url':pdf_url,'id':adminid})

def mem_notify(request):
    id = Member.objects.get(admin=request.user.id).id
    member=Member.objects.get(admin=request.user.id)
    isemployed=member.is_employed
    data=""
    # if isemployed == False:
    data=Notification.objects.filter(Q(mem_id=id) & Q(status='Pending'))
    return render(request,'MEMBERS/mem_notify.html',{'data':data,'isemployed':isemployed})

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
     user=Member.objects.filter(payment_id=order_id).first() 
     user.paid=True
     user.save()
 return render(request , 'MEMBERS/success.html',{'user':user})   






def member_login(request):
    return render(request,'MEMBERS/login2.html')


def doLogin(request):
    
        user=EmailBackEnd.authenticate(request,username=request.POST.get("adhaarNo"),password=request.POST.get("password"))
        if user!=None:
            
            if user.user_type=="4":
                if user.member.paid==1:
                    login(request,user)
                    return HttpResponseRedirect(reverse("member_dashboard"))
                else:
                    messages.error(request,'Access Denied')
                    return HttpResponseRedirect(reverse("member_login"))
             
                # return HttpResponseRedirect('/admin_home')
            # elif user.user_type=="2":
            #     return HttpResponseRedirect(reverse("staff_home"))
            # elif user.user_type=="4":
            #    # return HttpResponse("MEMBERS PANEL")
            #     return HttpResponseRedirect(reverse("dashboard"))
            # else:
            #     return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.warning(request,"Invalid adhaar number or password !!")
            return HttpResponseRedirect(reverse("member_login"))


# @login_required(login_url='member_login')

def dashboard(request):
    return render(request,'MEMBERS/dashboard.html')

def payment_information(request):

    member = Member.objects.filter(admin=request.user)

    return render(request,'MEMBERS/payment_info.html',{'member':member})


def member_profile(request):
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
            messages.success(request, "Your Profile Updated Successfully!!")
            return HttpResponseRedirect(reverse("member_profile"))
            # redirect('/')
            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
    return render(request,'MEMBERS/profile.html')  


def member_list(request,bookingid):
        count=request.session.get(f'request.user.id',None)
        employer=Employer.objects.get(admin=request.user.id)
        user=Booking.objects.get(id=bookingid)
        depttype=request.session.get('dept',None)
        roleId=request.session.get('roleId',None)
        if user.paid==1:   
            member = Member.objects.filter(Q(role_id_id=roleId) & Q(job_seeker=depttype) & Q(is_employed=False))
            if count +2 <= member.count():
                membertoShow=Member.objects.filter(Q(role_id_id=roleId) & Q(job_seeker=depttype) & Q(is_employed=False))[:count+2]
            elif count +1 == member.count():
                membertoShow=Member.objects.filter(Q(role_id_id=roleId) & Q(job_seeker=depttype) & Q(is_employed=False))[:count+1]
            else :
                membertoShow=Member.objects.filter(Q(role_id_id=roleId) & Q(job_seeker=depttype) & Q(is_employed=False))
            return render(request, 'MEMBERS/list.html',{'member':membertoShow,'count':count})    
        else :
            return redirect('employer_managebooking')
    