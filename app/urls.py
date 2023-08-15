from django.urls import path
from .import views,HOD_VIEWS,MEMBERS_VIEWS,EMPLOYEE_VIEWS,INSTRUCTOR_VIEWS,TRAINING_VIEWS
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from django.urls import re_path
from .MEMBERS_VIEWS import GeneratePDF

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('',views.home,name="home"),
    path('joblisting/',views.joblisting,name="joblisting"),
    path('jobdetails/<int:pk>',views.jobdetails,name="jobdetails"),
    path('course/',views.course,name="course"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('profile',views.profile,name="profile"),
    path('apply/',views.apply,name="apply"),
    path('gallery/',views.gallery,name="gallery"),
    path('manage_gallery/',views.manage_gallery,name="manage_gallery"),
    path('add_gallery/',views.add_gallery,name="add_gallery"),
    path('deleteimage/<str:id>',views.del_image,name="delete_image"),
    path('show_galary',views.show_galary,name="show_galary"),
    
  
    path('HOD/login2',HOD_VIEWS.login2, name="hod_login2"),
    path('HOD/dologin2',HOD_VIEWS.dologin2, name="hod_dologin2"),
    path('clc/',HOD_VIEWS.HOD,name="hod_dashboard"),
    path('HOD/Generic_Info',HOD_VIEWS.Generic_Info,name="Generic_Info"),
    path('HOD/add_city',HOD_VIEWS.ADD_CITY,name="add_city"),
    path('HOD/manage_city',HOD_VIEWS.MANAGE_CITY,name="manage_city"),
    path('HOD/edit_city/<int:id>',HOD_VIEWS.edit_city,name="edit_city"),
    path('HOD/edit_city',HOD_VIEWS.edit_city_save,name="edit_city_save"),
    path('HOD/manage_attendance',HOD_VIEWS.manage_attendance,name="hod_manageattendance"),
    path('HOD/manage_attendance/<int:id>',HOD_VIEWS.manage_individual,name="hod_manageindividual_atten"),
    path('HOD/manage_details',HOD_VIEWS.manage_details,name="hod_managedetails"),

    path('HOD/add_role',HOD_VIEWS.ADD_ROLE,name="add_role"),
    path('HOD/manage_role',HOD_VIEWS.MANAGE_ROLE,name="manage_role"),
    path('HOD/edit_role/<str:role_id>', HOD_VIEWS.edit_role,name="edit_role"),
    path('HOD/edit_role', HOD_VIEWS.edit_role_save,name="edit_rolee_save"),
    path('HOD/role/Delete/<int:role_id>', HOD_VIEWS.DELETE_ROLE,name="delete_role"),
    path('HOD/TRAINING',HOD_VIEWS.TRAINING_CENTER,name="training_center"),
    path('HOD/manage_center',HOD_VIEWS.MANAGE_CENTER,name="manage_center"),
    path('HOD/edit_center/<str:center_id>', HOD_VIEWS.edit_center,name="edit_center"),
    path('HOD/edit_center_save', HOD_VIEWS.edit_center_save,name="edit_center_save"),
    path('HOD/center/Delete/<str:center_id>', HOD_VIEWS.DELETE_CENTER,name="delete_center"),
    path('HOD/Location',HOD_VIEWS.LOCATION,name="location"),
    path('HOD/doLocation',HOD_VIEWS.doLocation,name="doLocation"),
    path('HOD/EmployeesSalary',HOD_VIEWS.employeesSalary,name="employeesSalary"),
    path('HOD/DoEmployeesSalary',HOD_VIEWS.doEmployeesSalary,name="doemployeesSalary"),
    


    path('HOD/add_employee',HOD_VIEWS.ADD_EMPLOYEE,name="add_employee"),
    path('do_employee_signup',HOD_VIEWS.do_employee_signup,name="do_employee_signup"),
    path('manage_employee',HOD_VIEWS.manage_employee,name="manage_employee"),
    path('HOD/edit_employee/<str:employee_id>', HOD_VIEWS.edit_employee,name="edit_employee"),
    path('HOD/edit_employee', HOD_VIEWS.edit_employee_save,name="edit_employee_save"),
    path('HOD/employee/Delete/<str:employee_id>', HOD_VIEWS.DELETE_EMPLOYEE,name="delete_employee"),


    path('HOD/add_instructor',HOD_VIEWS.ADD_INSTRUCTOR,name="add_instructor"),
    path('do_instructor_signup',HOD_VIEWS.do_instructor_signup,name="do_instructor_signup"),
    path('manage_instructor',HOD_VIEWS.manage_instructor,name="manage_instructor"),
    path('HOD/make_course', HOD_VIEWS.make_course,name="make_course"),
    path('HOD/edit_instructor/<str:instructor_id>', HOD_VIEWS.edit_instructor,name="edit_instructor"),
    path('HOD/edit_instructor', HOD_VIEWS.edit_instructor_save,name="edit_instructor_save"),
    # path('HOD/employee/Delete/<str:employee_id>', HOD_VIEWS.DELETE_EMPLOYEE,name="delete_emplo

    path('HOD/manage_members',HOD_VIEWS.manage_members,name="manage_members"),
    path('HOD/manage_members/payment_val/<int:id>',HOD_VIEWS.payment_val,name="payment_val"),
    path('HOD/courselist', HOD_VIEWS.courselist, name="courselist"),
    path('HOD/PaymentValidation',HOD_VIEWS.payment_validation,name="payment_validation"),
    



    ############################# MEMBER URL ###########################################
    
    path('register/',MEMBERS_VIEWS.register,name="register"),
    path('registration/pdf/', GeneratePDF.as_view(), name='generate_pdf'),
    path('dummy/',MEMBERS_VIEWS.dummy,name="dummy"),
    path('instantservice/',MEMBERS_VIEWS.instant_service,name="instant_register"),
    path('technicianlist/',MEMBERS_VIEWS.technicianlist,name="technician_list"),
    path('techniciandetail/<str:id>',MEMBERS_VIEWS.technician_detail,name="technician_detail"),
    path('douserregister/',MEMBERS_VIEWS.douserregister,name="douserregister"),
    path('success/', MEMBERS_VIEWS.Success , name='success'),
    path('MEMBERS/member_login', MEMBERS_VIEWS.member_login,name="member_login"),
    path('dologin/', MEMBERS_VIEWS.doLogin, name="dologin"),
    path('logout_user', views.logout_user,name="logout"),
   
    path('MEMBERS/Dashboard', MEMBERS_VIEWS.dashboard,name="member_dashboard"),
    path('MEMBERS/payment_information', MEMBERS_VIEWS.payment_information,name="payment_information"),
    path('MEMBERS/profile',MEMBERS_VIEWS.member_profile,name="member_profile"),
    path('MEMBERS/QR_Payment/<int:adminid>',MEMBERS_VIEWS.member_qr,name="member_qr"),
    path('MEMBERS/QR_Status/<int:adminid>',MEMBERS_VIEWS.qr_status,name="qr_status"),
    path('MEMBERS/list/<int:bookingid>',MEMBERS_VIEWS.member_list,name="member_list"),
    path('MEMBERS/mem_notify',MEMBERS_VIEWS.mem_notify,name="member_notify"),
    path('MEMBERS/mem_notify/<int:empid>/<str:status>',MEMBERS_VIEWS.emp_booked,name="emp_booked"),
    

    
    



    ########################## EMPLOYER URL ############################

    path('EMPLOYERS/booking', EMPLOYEE_VIEWS.emp_booking,name="emp_booking"),
    
    path('EMPLOYERS/Dashboard', EMPLOYEE_VIEWS.dashboard,name="dashboard"),
    path('EMPLOYERS/ADDBOOKING', EMPLOYEE_VIEWS.employer_addbooking,name="employer_addbooking"),
    path('EMPLOYERS/DOADDBOOKING', EMPLOYEE_VIEWS.employer_doaddbooking,name="employer_doAddBooking"),
    path('EMPLOYERS/MANAGEBOOKING', EMPLOYEE_VIEWS.employer_managebooking,name="employer_managebooking"),
    path('EMPLOYERS/DOEMPLOYEEBOOKING/<int:id>/<int:bookingid>',EMPLOYEE_VIEWS.employer_doempbooking,name="employer_dobooking"),
    path('EMPLOYERS/MANAGEATTENDANCE', EMPLOYEE_VIEWS.employer_manageattendance,name="employer_manageattendance"),
    path('EMPLOYERS/MANAGEATTENDANCE/<str:date>', EMPLOYEE_VIEWS.employer_manageindiv_atten,name="employer_manageindiv_atten"),
    path('EMPLOYERS/bookinglist', EMPLOYEE_VIEWS.employer_bookinglist,name="booking_list"),
    path('movies/add', EMPLOYEE_VIEWS.add_movie, name='add_movie'),
    path('EMPLOYERS/REGISTER', EMPLOYEE_VIEWS.employer_register,name="employer_register"),
    # path('EMPLOYERS/doregister', EMPLOYEE_VIEWS.employer_doregister,name="employer_doregister"),
    path('EMPLOYERS/login', EMPLOYEE_VIEWS.employer_login,name="employer_login"),
    path('EMPLOYERS/dologin', EMPLOYEE_VIEWS.employer_dologin,name="employer_dologin"),
    path('EMPLOYERS/profile',EMPLOYEE_VIEWS.employer_profile,name="employer_profile"),
    path('EMPLOYERS/memberList',EMPLOYEE_VIEWS.member_list,name="employer_memberList"),
    
    path('EMPLOYERS/login2',EMPLOYEE_VIEWS.login2, name="login2"),
    path('EMPLOYERS/dologin2',EMPLOYEE_VIEWS.dologin2, name="dologin2"),
    path('EMPLOYERS/service',EMPLOYEE_VIEWS.service, name="service"),
    path('Inner/service/',EMPLOYEE_VIEWS.manage_employer, name="manage_employer"),
    path('EmployerList/',EMPLOYEE_VIEWS.employerlist, name="employerlist"),
    path('Outer/service',EMPLOYEE_VIEWS.outer_employer_service, name="outer_employer_service"),
    path('Employer/Success',EMPLOYEE_VIEWS.emp_success,name="emp_success"),
    path('EMPLOYER/OUTER',EMPLOYEE_VIEWS.emp_outer,name="emp_outer"),
    path('EMPLOYER/do_OUTER',EMPLOYEE_VIEWS.do_emp_outer,name="do_emp_outer"),
    path('EMPLOYER/List_of_employer',EMPLOYEE_VIEWS.List_of_employer,name="List_of_employer"),
    path('EMPLOYER/emp_assign',EMPLOYEE_VIEWS.emp_assign,name="emp_assign"),
    path('EMPLOYER/emp_notify',EMPLOYEE_VIEWS.emp_notify,name="emp_notify"),
    path('EMPLOYER/MEMBERS_LIST',EMPLOYEE_VIEWS.members_list,name="emp_mem_list"),
    path('EMPLOYER/down-pdf',EMPLOYEE_VIEWS.down_pdf,name="down-pdf"),
    path('EMPLOYER/download_pdf/<int:id>',EMPLOYEE_VIEWS.download_pdf,name="download_pdf"),
    path('EMPLOYER/MEMBERSPAYMENT/<str:amount>/<str:month>',EMPLOYEE_VIEWS.mem_payment,name="mem_payment"),
    path('EMPLOYER/SalaryPayment/<str:amount>/<str:month>',EMPLOYEE_VIEWS.salarypayment,name="salary_payment"),
    path('EMPLOYER/MEMBERSPAYMENTSuccess/<str:month>/<int:emp_id>',EMPLOYEE_VIEWS.mem_paymentsuccess,name="mem_paymentsuccess"),
    
    
   




    path('worlker_list/<int:id>/<int:bookingid>',views.worlker_list,name="worlker_list"),
    path('booking_success/<int:bookingid>', views.booking_Success , name='bookingSuccess'),
    path('EMPLOYER/QR_Payment/<int:bookingid>',EMPLOYEE_VIEWS.qr_payment,name="qr_payment"),
    


    ########################## INSTRUCTOR URL ############################

    
    path('INSTRUCTOR/register', INSTRUCTOR_VIEWS.INSTRUCTOR_Register,name="INSTRUCTOR_Register"),
    path('INSTRUCTOR/doregister', INSTRUCTOR_VIEWS.INSTRUCTOR_doregister,name="INSTRUCTOR_doregister"),
    path('INSTRUCTOR/login', INSTRUCTOR_VIEWS.instructor_login,name="instructor_login"),
    path('INSTRUCTOR/dologin', INSTRUCTOR_VIEWS.instructor_dologin,name="instructor_dologin"),
    path('INSTRUCTOR/Dashboard', INSTRUCTOR_VIEWS.dashboard,name="instructor_dashboard"),
    path('INSTRUCTOR/add_course', INSTRUCTOR_VIEWS.add_course,name="add_course"),
    path('INSTRUCTOR/profile',INSTRUCTOR_VIEWS.INSTRUCTOR_profile,name="INSTRUCTOR_profile"),



    ################################## Training URL #####################   

    path('TRAINING/register', TRAINING_VIEWS.TRAINING_Register,name="TRAINING_Register"),
    path('do_training_register/',TRAINING_VIEWS.do_training_register,name="do_training_register"),
    path('Training/success/', TRAINING_VIEWS.Success , name='trainingsuccess'),
    path('TRAINING/login', TRAINING_VIEWS.TRAINING_login,name="TRAINING_login"),
    path('TRAINING/dologin/', TRAINING_VIEWS.training_doLogin, name="training_doLogin"),
    path('TRAINING/Dashboard', TRAINING_VIEWS.dashboard,name="training_dashboard"),
    path('TRAINING/process', TRAINING_VIEWS.TRAINING_process,name="TRAINING_process"),
    path('TRAINING/payment_information', TRAINING_VIEWS.training_payment_information,name="training_payment_information"),


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    


    path('register/success',views.success,name="succss"),
    path('testing',views.testing,name="testing"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)



# ==========================================Gallery====================================

