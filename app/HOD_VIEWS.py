from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import matplotlib.pyplot as plt
from app.models import*
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .globals import monthhh, set_month
import io
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.template.loader import get_template
import base64


def login2(request):
    return render(request, 'HOD/hod_login2.html')



def dologin2(request):
    if request.method == "POST":
        user=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect(reverse("hod_dashboard"))
                
            else:
                return redirect("hod_login2")
                # return HttpResponseRedirect(reverse("hod_login2"))
        else:
            messages.error(request,"Invalid Username and Password")
            return redirect("hod_login2")
            # return HttpResponseRedirect("hod_login2")

    return render(request, 'HOD/hod_login2.html')

@login_required(login_url='hod_dologin2')
def HOD(request):
    member_count=Member.objects.all().count()
    role_count=Role.objects.all().count()
    # data = [10, 20, 30, 40, 50]
    instructor_count=Instructor.objects.all().count()
    data = {
        'labels': ['Total profit in April', 'Total profit till March', 'Overall profit'],
        'values': [20000, 480000, 500000]
    }
    return render(request,'HOD/dashboard.html',{'member_count':member_count,'role_count':role_count,'instructor_count':instructor_count,'data':data})


def Generic_Info(request):
    return render(request,'HOD/generic_info.html')
def ADD_CITY(request):
    if request.method == "POST":
        city = request.POST.get('city')
        if City.objects.filter(city = city).exists():
                messages.warning(request,city + " is already Taken ")
                return redirect('add_city')
        try:
            city = City.objects.create(city=city)
            city.save()
            messages.success(request,"Successfully Created City")
            return HttpResponseRedirect(reverse("manage_city"))
        except:
            messages.error(request,"Failed to Create City")
            return HttpResponseRedirect(reverse("add_city"))
    return render(request,'HOD/add_city.html')

def MANAGE_CITY(request):
    city = City.objects.all()
    if request.method == "POST":
        active_list = request.POST.getlist('active')
        city.update(active=False)
        for activee in active_list:
            City.objects.filter(id= int(activee)).update(active=True)
    return render(request,'HOD/manage_city.html',{'city':city})

def edit_city(request,id):
    city = City.objects.get(id=id) 
    return render(request,'HOD/edit_city.html',{'city':city})

def edit_city_save(request):
    if request.method == "POST":
        city_id = request.POST.get('city_id')
        city_name = request.POST.get('city')
        try:
            city=City.objects.get(id=city_id)
            city.city=city_name
            city.save()
            messages.success(request,"Successfully Edited City")
            return HttpResponseRedirect(reverse("manage_city"))
        except:
            messages.error(request,"Failed to Edit City")
            return HttpResponseRedirect(reverse("manage_city"))
        

    return render(request,'HOD/manage_city.html')    

def manage_attendance(request):
    data=Member.objects.all()
    return render(request,'HOD/manage_attendance.html',{'data':data})

def manage_individual(request,id):
    filteredData=Attendance.objects.filter(person_id=id)
    return render(request,'HOD/manage_individual.html',{'filteredData':filteredData})

def ADD_ROLE(request):
    city_name = City.objects.all()
    if request.method == 'POST':
        role = request.POST.get('role')
        city = request.POST.get('city')
        min_salary = request.POST.get('min_salary')
        max_salary = request.POST.get('max_salary')
        gov_approved = request.POST.get('gov_approved')
        margin = request.POST.get('margin')

        cityy = City.objects.get(id=city)

        try:
            
            # if Role.objects.filter(role_name = role).exists():
            #     messages.warning(request,role + " is already Taken ")
            #     return redirect('add_role')
            rolee = Role.objects.create(role_name=role,city=cityy,min_sal=min_salary,max_sal=max_salary,gov_approved=gov_approved,margin=margin)
            rolee.save()
            messages.success(request,"Successfully Created Role")
            return HttpResponseRedirect(reverse("manage_role"))
        except:
            messages.error(request,"Failed to Create Role")
            return HttpResponseRedirect(reverse("add_role"))

    return render(request,'HOD/add_role.html',{'city':city_name})

def MANAGE_ROLE(request):
    role = Role.objects.all()
    
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        id_list2 = request.POST.getlist('boxes2')
        # active_list = request.POST.getlist('active')
        # print(active_list)
        role.update(is_worker=False)
        role.update(is_employer=False)
        # role.update(active=False)
        for x in id_list:
            Role.objects.filter(id= int(x)).update(is_worker=True)
        for y in id_list2:
            Role.objects.filter(id= int(y)).update(is_employer=True)
        # for activee in active_list:
        #     City.objects.filter(id= int(activee)).update(active=True)
            

    return render(request,'HOD/manage_roll.html',{'role':role})


def edit_role(request,role_id):
    role=Role.objects.get(id=role_id)
    return render(request,"HOD/edit_role.html",{"role":role,"id":role_id})

def manage_details(request):
    if request.method=="POST":
        data=Notification.objects.filter(status='Accepted')
        month = request.POST.get('month')
        emp_visibility=request.POST.get('emp_visibility')
        settings, created = GlobalSettings.objects.get_or_create(pk=1)
        settings.month = month
        settings.save()
        if emp_visibility == "Show":
            for i in data:
                i.emp_paid=False
                i.save()
        else:
            for i in data:
                i.emp_paid=True
                i.save() 
    return render(request,'HOD/manage_details.html')


def edit_role_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        role_id=request.POST.get("role_id")
        role_name=request.POST.get("role_name")
        # last_name=request.POST.get("lname")
        # email=request.POST.get("email")
        # username=request.POST.get("username")
        # address=request.POST.get("address")

        if Role.objects.filter(role_name = role_name).exists():
                messages.warning(request,role_name + " is already Taken ")
                return redirect('manage_role')

        try:
            user=Role.objects.get(id=role_id)
            user.role_name=role_name
            # user.last_name=last_name
            # user.email=email
            # user.username=username
            user.save()

            # employee_model=Employee.objects.get(admin=employee_id)
            # employee_model.address=address
            # employee_model.save()
            messages.success(request,"Successfully Edited Employee")
            return HttpResponseRedirect(reverse("manage_role"))
        except:
            messages.error(request,"Failed to Edit Employee")
            return HttpResponseRedirect(reverse("manage_role"))



def DELETE_ROLE(request,role_id):
    
    # agent = SuperAgent.objects.get(admin=id)
    role = Role.objects.get(id=role_id)
    role.delete()
    messages.success(request,"Record is Successfully Deleted")
    return redirect('manage_role')


def employeesSalary(request):
    return render(request,'HOD/employeesalary.html')

def doEmployeesSalary(request):
    if request.method == "POST":
        month=request.POST.get("month")
        data=AttendancePDFForm.objects.filter(month=month)
        context={
            'data':data,
        }
    return render(request,'HOD/employeesalary.html',context)

def payment_val(request,id):
    mem=Member.objects.get(id=id)
    print(request.GET)
    status = request.GET.get('status')
    if status=='accept':
        mem.paid=1 
        messages.success(request,f" {mem.admin}'s Access has been approved") 
    elif status=='reject':
        mem.paid=0
        messages.error(request,f" {mem.admin}'s Access has been declined")
    mem.save()
    
    return redirect('manage_members')
    # return render(request,'HOD/why.html')


def payment_validation(request):
    data=SalaryValidation.objects.all()
    if request.method=="POST":
        action=request.POST.get('validation')
        payment_id=request.POST.get('payment_id')
        remark=request.POST.get('remark')
        validated_entry=SalaryValidation.objects.get(payment_id=payment_id)
        validated_entry.is_validated=True
        validated_entry.save()
        mem_data=AttendancePDFForm.objects.filter(payment_id=payment_id)
        for i in mem_data:
            i.remark=remark
            i.paid_status=action
            i.save()
    context={
        'data':data,
    }

    return render(request,'HOD/payment_validation.html',context)

def ADD_EMPLOYEE(request):

    return render(request,'HOD/add_employee.html')



def do_employee_signup(request):
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email,user_type=2)
        user.employee.address=address
        user.save()
        messages.success(request,"Successfully Created Employee")
        return HttpResponseRedirect(reverse("add_employee"))
    except:
        messages.error(request,"Failed to Create Employee")
        return HttpResponseRedirect(reverse("add_employee"))


def manage_employee(request):
    employee=Employer.objects.all()
    return render(request,"HOD/manage_employee.html",{"employee":employee})

def edit_employee(request,employee_id):
    employee=Employer.objects.get(admin=employee_id)
    return render(request,"HOD/edit_employee.html",{"employee":employee,"id":employee_id})


def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.POST.get("employee_id")
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=employee_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            employee_model=Employer.objects.get(admin=employee_id)
            employee_model.address=address
            employee_model.save()
            messages.success(request,"Successfully Edited Employee")
            return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
        except:
            messages.error(request,"Failed to Edit Employee")
            return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))



def DELETE_EMPLOYEE(request,employee_id):
    
    # agent = SuperAgent.objects.get(admin=id)
    employee = CustomUser.objects.get(id=employee_id)
    employee.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('manage_employee')





######################## Instructor ##############################

def ADD_INSTRUCTOR(request):
    return render(request,'HOD/add_instructor.html')


def make_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        practical_equip_names = request.POST.getlist('practical_equip')
        theory_equip_names = request.POST.getlist('theory_equip')
        assessment_equip_names = request.POST.getlist('assessment_equip')

        # # Create the course
        # course = courseaddition.objects.create(name=name)
        # for equip_name in practical_equip_names:
        #     equipment, _ = PracEquipment.objects.get_or_create(name=equip_name)
        #     course.practical_equip.add(equipment)
        
        # for equip_name in theory_equip_names:
        #     equipment, _ = TheoryEquipment.objects.get_or_create(name=equip_name)
        #     course.theory_equip.add(equipment)

        # for equip_name in assessment_equip_names:
        #     equipment, _ = AssessEquipment.objects.get_or_create(name=equip_name)
        #     course.assessment_equip.add(equipment)
        
        # Get the equipment objects for each category
        # practical_equip = Equipment.objects.filter(name__in=practical_equip_names)
        # theory_equip = Equipment.objects.filter(name__in=theory_equip_names)
        # assessment_equip = Equipment.objects.filter(name__in=assessment_equip_names)
        # print(practical_equip_names)
        # # Set the equipment values
        # course.practical_equip.set(practical_equip)
        # course.theory_equip.set(theory_equip)
        # course.assessment_equip.set(assessment_equip)
    return render(request,'HOD/make_course.html')

def do_instructor_signup(request):
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email,user_type=3)
        user.instructor.address=address
        user.save()
        messages.success(request,"Successfully Created Instructor")
        return HttpResponseRedirect(reverse("add_instructor"))
    except:
        messages.error(request,"Failed to Create Employee")
        return HttpResponseRedirect(reverse("add_instructor"))





def manage_instructor(request):
    instructor=Instructor.objects.all()
    return render(request,"HOD/manage_instructor.html",{"instructor":instructor})



def edit_instructor(request,instructor_id):
    instructor=Instructor.objects.get(admin=instructor_id)
    return render(request,"HOD/edit_instructor.html",{"instructor":instructor,"id":instructor_id})






def edit_instructor_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        instructor_id=request.POST.get("instructor_id")
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=instructor_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            employee_model=Instructor.objects.get(admin=instructor_id)
            employee_model.address=address
            employee_model.save()
            messages.success(request,"Successfully Edited Instructor")
            return HttpResponseRedirect(reverse("edit_instructor",kwargs={"instructor_id":instructor_id}))
        except:
            messages.error(request,"Failed to Edit Instructor")
            return HttpResponseRedirect(reverse("edit_instructor",kwargs={"instructor_id":instructor_id}))



def manage_members(request):
    member = Member.objects.all()
    
    return render(request,'HOD/manage_members.html',{'member':member})



def TRAINING_CENTER(request):
    if request.method == 'POST':
        center_name = request.POST.get('training')

        try:
            
            if Center.objects.filter(center_name = center_name).exists():
                messages.warning(request,center_name + " is already Taken ")
                return redirect('training_center')
            center = Center.objects.create(center_name=center_name)
            center.save()
            messages.success(request,"Successfully Created Center")
            return HttpResponseRedirect(reverse("training_center"))
        except:
            messages.error(request,"Failed to Create Role")
            return HttpResponseRedirect(reverse("training_center"))

    return render(request,'HOD/training.html')


def MANAGE_CENTER(request):
    center = Center.objects.all()
    return render(request,'HOD/manage_center.html',{'center':center})



def edit_center(request,center_id):
    center=Center.objects.get(id=center_id)
    return render(request,"HOD/edit_role.html",{"center":center,"id":center_id})



def edit_center_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        center_id=request.POST.get("center_id")
        center_name=request.POST.get("center_name")
        # last_name=request.POST.get("lname")
        # email=request.POST.get("email")
        # username=request.POST.get("username")
        # address=request.POST.get("address")

        try:
            center=Center.objects.get(id=center_id)
            center.center_name=center_name
            # user.last_name=last_name
            # user.email=email
            # user.username=username
            center.save()

            # employee_model=Employee.objects.get(admin=employee_id)
            # employee_model.address=address
            # employee_model.save()
            messages.success(request,"Successfully Updated Center")
            return HttpResponseRedirect(reverse("manage_center"))
        except:
            messages.error(request,"Failed to Updated Center")
            return HttpResponseRedirect(reverse("manage_center"))




def DELETE_CENTER(request,center_id):
    
    # agent = SuperAgent.objects.get(admin=id)
    center = Center.objects.get(id=center_id)
    center.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('manage_center')


def LOCATION(request):

    center = Center.objects.all()
    return render(request,'HOD/location.html',{'center':center})

def doLocation(request):
    if request.method == "POST":
        center_id = request.POST.get('center_id')
        location = request.POST.get('location')
        center=Center.objects.get(id=center_id)

        loc = Location.objects.create(center_name=center,location=location)
        loc.save()

        

    return render(request,'HOD/location.html')



# COURSE LIST VIEWS START

def courselist(request):
    course = Course.objects.all()
    return render(request, "HOD/courselist.html", {"course":course})


# COURSE LIST VIEWS END

