# from msilib.schema import File
from pydoc import render_doc
import requests
import json
import razorpay
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.models import *
from django.contrib import messages
from app.EmployerEmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import FileResponse
from .globals import monthhh
from django.views.decorators.csrf import csrf_exempt



def dashboard(request):
    return render(request, 'employer/dashboard.html')

def employer_addbooking(request):
    role = Role.objects.all()
    city = City.objects.all()
    # if request.method == "POST":

    #     services = request.POST.get('service')
    #     no_of_worker = request.POST.get('no_of_worker')
    #     gender = request.POST.get('gender')
    #     start_Date = request.POST.get('start_Date')
    #     landmark = request.POST.get('landmark')
    #     city = request.POST.get('city')
    #     state = request.POST.get('state')
    #     pin = request.POST.get('pin')
    #     anyother = request.POST.get('anyother')
    #     salary = request.POST.get('salary')
    #     goverment = request.POST.get('goverment')
    #     department = request.POST.get('dep_name')

    #     role_id = Role.objects.get(id=services)
    #     # print("roleeeeeeeeeeeeeeee",role_id.id)
    #     # role = Role.objects.get()

    #     employer_obj = Employer.objects.get(admin=request.user.id)

    #     booking = Booking.objects.create(employer_id=employer_obj, services=role_id, no_of_worker=no_of_worker, gender_preference=gender, work_start_Date=start_Date,
    #                                      landmark=landmark, city=city, state=state, pin_code=pin, specific_requirements=anyother, sallery_offerd=salary, goverment=goverment, department=department)
    #     booking.save()

    #     messages.success(request, "Successfully Created employer")
    city_name = ""
    role_final=""
    if request.method=="POST":
        city_search=request.POST.get('city_search')
        city_name=City.objects.get(id=city_search)
        role_final=Role.objects.filter(city_id=city_search)

    return render(request, 'employer/add_booking.html', {'role': role,'city':city,'city_name':city_name,'role_final':role_final})

def employer_doaddbooking(request):
    role=Role.objects.all()
    if request.method == "POST":

        services = request.POST.get('service')
        no_of_worker = int(request.POST.get('no_of_worker'))
        gender = request.POST.get('gender')
        start_Date = request.POST.get('start_Date')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        anyother = request.POST.get('anyother')
        salary = int(request.POST.get('salary'))
        salary_temp=Role.objects.get(id=services)
        salary1=int(salary_temp.max_sal)
        total_monthly = int(no_of_worker * salary1)
        goverment = request.POST.get('goverment2')
        department = request.POST.get('dep_name')
        role_id = Role.objects.get(id=services)
        employer_obj = Employer.objects.get(admin=request.user.id)
        if department == "":
            department = "Private"
        booking = Booking.objects.create(employer_id=employer_obj, services=role_id, no_of_worker=no_of_worker, gender_preference=gender, work_start_Date=start_Date, landmark=landmark,
                                         city=city, state=state, pin_code=pin, specific_requirements=anyother, sallery_offerd=salary1, goverment=goverment, department=department, total_monthly=total_monthly)

        booking.save()
        messages.success(request, "Successfully Booking For Employer")
        return redirect('employer_addbooking')
    return render(request,'employer/add_booking.html',{'role':role,'city':city})



def employer_managebooking(request):
    booking = Employer.objects.get(admin=request.user.id)
    booking_data = Booking.objects.filter(employer_id=booking)
    return render(request, 'employer/emp_manage_booking.html', {'booking_data': booking_data})

def members_list(request):
    emp_id = Employer.objects.get(admin=request.user.id).id
    data=Notification.objects.filter(Q(status='Accepted') & Q(emp_id=emp_id))
    settings = GlobalSettings.objects.get(pk=1)
    month = settings.month
    emp_name=Employer.objects.get(admin=request.user.id).admin.username
    amount=0
    filtered_data=AttendancePDFForm.objects.filter(Q(month=month) & Q(payment_id__exact=None) & Q(emp_id=emp_id)) 
    print(filtered_data)
    for i in filtered_data:
        amount=amount+i.amount
    if request.method=="POST":
        id=request.POST.get('id')
        mem_name=request.POST.get('name')
        no_of_days=request.POST.get('no_of_days')
        month=month
        pdf_file1=request.FILES.get('salary')
        sal_amount=float(no_of_days)*(9000/30)
        salary_receipt=AttendancePDFForm.objects.create(month=month,no_of_days=no_of_days,pdf_file=pdf_file1,mem_id=id,mem_name=mem_name,org_name=emp_name,amount=sal_amount,emp_id=emp_id)
        salary_receipt.save()
        messages.success(request,'Your File has been uploaded.')
        filtered_data=AttendancePDFForm.objects.filter(Q(month=month) & Q(payment_id__exact=None) & Q(emp_id=emp_id)) 
        for i in filtered_data:
            amount=amount+i.amount
        return render(request,'employer/emp_mem_list.html',{'data':data,'month':month,'amount':amount})

    return render(request,'employer/emp_mem_list.html',{'data':data,'month':month,'amount':amount})
def mem_payment(request,amount,month):
    payment=""
    emp_id = Employer.objects.get(admin=request.user.id).id
    # client=razorpay.Client(auth=("rzp_test_c9U71b8iZvSlxi" , "DkSl2ey8clwF0dtmPlq73QUe"))
    amount=amount
    total=amount*100
    # payment=client.order.create({'amount':total, 'currency':'INR' , 'payment_capture' : '1'})
    return render(request,'employer/mem_payment.html',{'amount':amount,'month':month,'emp_id':emp_id})


def down_pdf(request):
    pdf_file = open('static/attendance_pdf/format.pdf', 'rb')
    return FileResponse(pdf_file, as_attachment=True, filename='salary_format.pdf')

def qr_payment(request,bookingid):
    context={
        'bookingid':bookingid,
    }
    return render(request,'employer/qr_payment.html',context)
# @csrf_exempt
def mem_paymentsuccess(request,month,emp_id):
    a=request.POST
    order_id=""
    # emp_id = Employer.objects.get(admin=request.user.id).id
    # for key,val in a.items():
    #     if key=="razorpay_order_id":
    #         order_id = val
    #         break
    order_id=request.POST.get('payment_id')
    org_name = Employer.objects.get(admin=request.user.id).admin.username
    data=Notification.objects.filter(Q(status='Accepted') & Q(emp_id=emp_id) & Q(emp_paid=False))
    data_month=AttendancePDFForm.objects.filter(Q(month=month) & Q(emp_id=emp_id) & Q(payment_id__exact=None))
    payment_upload=SalaryValidation.objects.create(emp_id=emp_id,org_name=org_name,month=month,payment_id=order_id)
    payment_upload.save()
    if request.method== "POST":
        for i in data:
            i.emp_paid=True
            i.save()
        # data.save()
        for i in data_month:
            i.paid_status='Pending'
            i.payment_id=order_id
            i.save()
        # data_month.save()
    return render(request,'employer/mem_paymentsuccess.html')

def download_pdf(request,id):
    name=Notification.objects.get(mem_id=id).name
    if request.method=="POST":
        org_name=request.POST.get('org_name')
        month=request.POST.get('month')
        no_of_days=request.POST.get('no_of_days')
        pdf_file1=request.FILES.get('salary')
        salary_receipt=AttendancePDFForm.objects.create(org_name=org_name,month=month,no_of_days=no_of_days,pdf_file=pdf_file1)
        salary_receipt.save()
        messages.success(request,'Your File has been uploaded.')
    return render(request,'employer/download_pdf.html',{'id':id,'mem_name':name})



def employer_bookinglist(request):

    booking = Employer.objects.get(admin=request.user.id)
    # print(booking)
    booking_data = Booking.objects.filter(employer_id=booking)
    print(booking_data)

    return render(request, 'employer/booking_list.html', {'booking_data': booking_data, 'booking': booking})

def employer_doempbooking(request,id,bookingid):
    booking = Employer.objects.get(admin=request.user.id)
    monthly = Booking.objects.get(id=bookingid)
    count=monthly.no_of_worker
    monthly_offered=monthly.sallery_offerd
    emp_gov=Employer.objects.get(admin=request.user.id)
    depttype=emp_gov.section
    member = Member.objects.filter(Q(role_id_id=id) & Q(job_seeker=depttype))
    membercount=member.count()
    if membercount>=int(count) :    
        no_of_emp=count
    else :
        no_of_emp=membercount
    # client=razorpay.Client(auth =("rzp_test_czVP739sBN5blU" , "MBpgYsg92tAkraZtv5BMyLeq"))
    amount=int(no_of_emp)*int(monthly_offered)
    total=amount*100
    # payment=client.order.create({'amount':total, 'currency':'INR' , 'payment_capture' : '1'})
    request.session[f'request.user.id']= int(no_of_emp)
    request.session['roleId']=id
    request.session['dept']=depttype
    request.session.save()
    return render(request,'employer/doempbooking.html',{'no_of_emp':no_of_emp,'monthly_offered':monthly_offered,'amount':amount,'bookingid':bookingid})


def employer_manageattendance(request):
    today = datetime.now().date()
    dates = [today - timedelta(days=x) for x in range(30)]
    return render(request, 'employer/emp_manage_attendance.html', {'dates': dates})


def employer_manageindiv_atten(request, date):
    data = Member.objects.all()
    if request.method == "POST":
        for person in data:
            atten = request.POST.get(f'{person.id}')
            if atten == 'present':
                atten = 'True'
            else:
                atten = 'False'
            if Attendance.objects.filter(date=date, name=person.admin,person_id=person.id).exists():
                entry=Attendance.objects.get(date=date,name=person.admin,person_id=person.id)
                entry.attendance=atten
                entry.save() 
            else:
                entry = Attendance.objects.create( name=f'{person.admin}', date=date, attendance=atten,person_id=person.id)
                entry.save()
        messages.success(request, f'Attendance has been marked for {date}')
        return redirect('employer_manageattendance')

    return render(request, 'employer/emp_individuals.html', {'date': date, 'data': data})


def member_list(request):
    return render(request,'memberList.html')

def add_movie(request):
    return render(request, 'add_movie.html')



def employer_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        emp_city = request.POST.get('emp_city')
        emp_state = request.POST.get('emp_state')
        emp_pin = request.POST.get('emp_pin')
        emp_pan = request.POST.get('emp_pan')
        address = request.POST.get('address')
        pan_no = request.FILES.get('pan_no')
        goverment = request.POST.get('goverment')
        password = request.POST.get("mobile_no")
        # print("ddddddddddddddddddddddddddddd",emp_pan)
        if CustomUser.objects.filter(pan_no=emp_pan).exists():
            messages.warning(request, "Pan Number is already Taken")
            return redirect('employer_register')

        if Employer.objects.filter(mob_no=password).exists():
            messages.warning(request, "Mobile Number is already Taken")
            return redirect('employer_register')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('employer_register')

        userr = CustomUser.objects.create_user(
            username=username, password=password, pan_no=emp_pan, user_type=2)

        userr.employer.mob_no = password
        userr.employer.emp_city = emp_city
        userr.employer.emp_state = emp_state
        userr.employer.emp_pin_code = emp_pin
        userr.employer.pan_no = emp_pan
        userr.employer.pan_Card = pan_no
        userr.employer.section = goverment
        userr.employer.address = address

        userr.save()
        user = EmailBackEnd.authenticate(
            request, username=emp_pan, password=password)
        if user != None:
            login(request, user)
            if user.user_type == "2":
                return HttpResponseRedirect(reverse("emp_outer"))
            # else:
            #     return HttpResponseRedirect(reverse("login2"))
        else:
            messages.error(request, "Invalid Login Details")
            # messages.success(request,"Successfully Created Employer")
            return HttpResponseRedirect(reverse("emp_outer"))

    return render(request, 'employer/register.html')


# def employer_doregister (request):
#     fname=request.POST.get("fname")
#     lname=request.POST.get("lname")
#     username=request.POST.get("username")
#     email=request.POST.get("email")
#     password=request.POST.get("password")
#     address=request.POST.get("address")

#     try:
#         user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email,user_type=2)
#         user.employee.address=address
#         user.save()
#         messages.success(request,"Successfully Created Employee")
#         # return HttpResponse("success")
#         return HttpResponseRedirect(reverse("employer_login"))
#     except:
#         messages.error(request,"Failed to Create Employee")

#         return HttpResponseRedirect(reverse("employer_register"))


def employer_login(request):
    return render(request, 'employer/login.html')


def employer_dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # captcha_token = request.POST.get("g-recaptcha-response")
        # cap_url = "https://www.google.com/recaptcha/api/siteverify"
        # cap_secret = "6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data = {"secret": cap_secret, "response": captcha_token}
        # cap_server_response = requests.post(url=cap_url, data=cap_data)
        # cap_json = json.loads(cap_server_response.text)

        # if cap_json['success'] == False:
        #     messages.error(request, "Invalid Captcha Try Again")
        #     return HttpResponseRedirect(reverse("employer_login"))
        #     # return HttpResponseRedirect("employer_login")

        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "username"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "2":
                return HttpResponseRedirect(reverse("dashboard"))
            else:
                return HttpResponseRedirect(reverse("employer_login"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("employer_login")


def employer_profile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # print(first_name)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("profile"))
            # redirect('/')

        except:
            messages.error(request, "Failed to Update Your Profile")
    return render(request, 'employer/profile.html')

def emp_assign(request):
    if request.method=='POST':
        selected_buttons = request.POST.get('selected_buttons', '').split(',')
        emp_id = Employer.objects.get(admin=request.user.id).id
        emp_name=Employer.objects.get(id=emp_id)
        members=[]
        for mem_id in selected_buttons:
            member=Member.objects.get(id=mem_id)
            notification=Notification.objects.create(name=member.admin.username,emp_id=emp_id,mem_id=mem_id,status='Pending',emp_name=emp_name.admin.username,message=f'You have been Requested to be employed by {emp_name.admin.username}',emp_city=emp_name.emp_city,emp_address=emp_name.address)
            members.append(member)
            notification.save()
        
        # for i in selected_buttons:
            
    return render(request,'employer/emp_assign.html',{'members':members})

def emp_notify(request):
    id = Employer.objects.get(admin=request.user.id).id
    data=Notification.objects.filter(emp_id=id)
    return render(request,'employer/emp_notify.html',{'data':data})

def salarypayment(request,amount,month):
    id = Employer.objects.get(admin=request.user.id).id
    return render(request,'employer/salary_payment.html',{'month':month,'emp_id':id})



def login2(request):
    return render(request, 'employer/employer_login2.html')


def dologin2(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "pan_no"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "2":
                return HttpResponseRedirect(reverse("emp_outer"))

            else:
                return HttpResponseRedirect(reverse("login2"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("login2")

    return render(request, 'employer/employer_login2.html')


def service(request):

    role = Role.objects.all()
    # if request.method == "POST":
    #     services = request.POST.get('service')
    #     gender = request.POST.get('gender')
    #     start_Date = request.POST.get('start_Date')
    #     landmark = request.POST.get('landmark')
    #     city = request.POST.get('city')
    #     state = request.POST.get('state')
    #     pin = request.POST.get('pin')
    #     salary = request.POST.get('salary')
    #     anyother = request.POST.get('anyother')
    #     no_of_worker = request.POST.get('no_of_worker')

    #     username=request.POST.get("username")

    #     fathername=request.POST.get("father_name")
    #     mobile_no=request.POST.get("mobile_no")
    #     emp_gender=request.POST.get("emp_gender")
    #     emp_city=request.POST.get("emp_city")
    #     emp_state=request.POST.get("emp_state")
    #     emp_pin=request.POST.get("emp_pin")
    #     emp_location=request.POST.get("emp_location")
    #     emp_aadhar=request.POST.get("emp_aadhar")
    #     emp_pan=request.POST.get("emp_pan")
    #     emp_aadhar_photo=request.FILES.get("emp_aadhar_photo")
    #     emp_pan_photo=request.FILES.get("emp_pan_photo")
    #     goverment = request.POST.get('goverment')
    #     password=request.POST.get("password")
    #     address=request.POST.get("address")
    #     pan_no = request.FILES.get('pan_no')

    #     # service = Role.objects.get(id=services)
    #     # print("sssssssssssssssssssssssssssssss",service)

    #     # print("first name =",fname,"last name =",lname,"father name =",fathername,"mobile no=",mobile_no,"employee gender = ",emp_gender,"employee date of birth =",dob,"employee city =",emp_city,"emp state = ",emp_state,"emp_pin =",emp_pin,"email=",email,'password=',password,"address=",address,"pan_no=",pan_no)
    #     # print("serviceeeeeeeeeeeeeeeeeeeeeeee",services)
    #     # serv = Role.objects.get(id=services)

    #     user=CustomUser.objects.create_user(username=username,password=password,user_type=2)

    #     user.employer.services  = services
    #     user.employer.gender_preference  = gender
    #     user.employer.work_start_Date  = start_Date
    #     user.employer.landmark  = landmark
    #     user.employer.city  = city
    #     user.employer.state  = state
    #     user.employer.pin_code  = pin
    #     user.employer.sallery_offerd  = salary
    #     user.employer.specific_requirements  = anyother
    #     user.employer.no_of_worker  = no_of_worker

    #     user.employer.fathername  = fathername
    #     user.employer.mob_no  = mobile_no
    #     user.employer.emp_gender  = emp_gender
    #     user.employer.emp_city  = emp_city
    #     user.employer.emp_state  = emp_state
    #     user.employer.emp_pin_code  = emp_pin
    #     user.employer.location  = emp_location
    #     user.employer.adhaar_no  = emp_aadhar
    #     user.employer.pan_no  = emp_pan
    #     user.employer.adhar_Card  = emp_aadhar_photo
    #     user.employer.pan_Card  = emp_pan_photo

    #     user.save()
    #     messages.success(request,"Successfully Created employer")

    return render(request, 'employer/employer_service.html', {'role': role})
    # return render(request, 'employer/employer_service.html',{'role':role})


def emp_booking(request):
    role = Role.objects.all()
    return render(request, 'employer/booking.html', {'role': role})


def manage_employer(request):
    # role = Role.objects.get(id=id)
    # book = Booking.objects.filter(services=role)

    employer = Booking.objects.all().order_by('-id')
    # b = Booking.objects.filter(services=id)

    return render(request, 'employer/manage_service.html', {'employer': employer})


def employerlist(request):
    employer = Booking.objects.all().order_by('-id')
    return render(request, 'HOD/employerlist.html', {'employer': employer})


def outer_employer_service(request):
    outr = outer.objects.all().order_by('-id')
    city = City.objects.all()
    return render(request, 'employer/emp_outer_manage.html', {'outr': outr, 'city': city})


@login_required(login_url="login2")
def emp_outer(request):
    payout = request.GET.get('city')
    employer_obj = Employer.objects.get(admin=request.user.id)
    sectn = employer_obj.section

    # print("userrrrrrrrrr",user)

    city = City.objects.all()
    role = Role.objects.all()
    demo3 = ""
    city_search = ""
    city_name = ""
    if request.method == "POST":
        role3 = request.POST.get('testing')
        print("roleeeee", role3)
        city_search = request.POST.get('city_search')
        cityy = City.objects.get(id=role3)
        role2 = Role.objects.filter(city_id=cityy)
        demo3 = role2
        city_name = City.objects.get(id=city_search)
    return render(request, "employer/outer.html", {'role': role, 'city': city, 'demo': demo3, 'city_name': city_name, 'employer_obj': employer_obj, 'sectn': sectn})


def do_emp_outer(request):
    if request.method == "POST":

        services = request.POST.get('service')
        no_of_worker = int(request.POST.get('no_of_worker'))
        gender = request.POST.get('gender')
        start_Date = request.POST.get('start_Date')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        anyother = request.POST.get('anyother')
        # salary = int(request.POST.get('salary'))
        salary_temp=Role.objects.get(id=services)
        salary1=int(salary_temp.max_sal)
        total_monthly = int(no_of_worker * salary1)
        print("totalllllllll", total_monthly)
        goverment = request.POST.get('goverment2')
        department = request.POST.get('dep_name')

        if department == "":
            department = "Private"
            print("sssssssssss", department)
        # name = request.POST.get('name')
        # mobile_no = request.POST.get('mobile_no')
        role_id = Role.objects.get(id=services)
        employer_obj = Employer.objects.get(admin=request.user.id)
        booking = Booking.objects.create(employer_id=employer_obj, services=role_id, no_of_worker=no_of_worker, gender_preference=gender, work_start_Date=start_Date, landmark=landmark,
                                         city=city, state=state, pin_code=pin, specific_requirements=anyother, sallery_offerd=salary1, goverment=goverment, department=department, total_monthly=total_monthly)

        booking.save()
        messages.success(request, "Successfully Booking For Employer")
        return redirect('emp_outer')

        # outer_booking = outer.objects.create(name=name,mob=mobile_no,services=services,no_of_worker=no_of_worker,gender_preference=gender,work_start_Date=start_Date,landmark=landmark,city=city,state=state,pin_code=pin,specific_requirements=anyother,sallery_offerd=salary,goverment=goverment,department=department)
        # outer_booking.save()

        # messages.success(request,"Successfully Created employer")
    return render(request, "employer/outer.html", {'city': city})

def List_of_employer(request):
    employer = Employer.objects.all()
    return render(request, 'employer/list_of_employer.html', {'employer': employer})


@login_required(login_url="/EMPLOYERS/login2")
def emp_success(request):

    if request.method == "POST":

        services = request.POST.get('service')
        no_of_worker = request.POST.get('no_of_worker')
        gender = request.POST.get('gender')
        start_Date = request.POST.get('start_Date')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        anyother = request.POST.get('anyother')
        salary = request.POST.get('salary')
        goverment = request.POST.get('goverment')
        department = request.POST.get('dep_name')

        employer_obj = Employer.objects.get(admin=request.user.id)

        booking = Booking.objects.create(employer_id=employer_obj, services=services, no_of_worker=no_of_worker, gender_preference=gender, work_start_Date=start_Date,
                                         landmark=landmark, city=city, state=state, pin_code=pin, specific_requirements=anyother, sallery_offerd=salary, goverment=goverment, department=department)
        booking.save()

        messages.success(request, "Successfully Created employer")

    return render(request, 'employer/success.html')
