from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "app.HOD_VIEWS":
                    pass
                elif modulename == "app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("hod_dashboard"))
            elif user.user_type == "2":
                if modulename == "app.EMPLOYEE_VIEWS" or modulename == "app.EditResultVIewClass":
                    pass
                elif modulename == "app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "3":
                if modulename == "app.INSTRUCTOR_VIEWS" or modulename == "django.views.static":
                    pass
                elif modulename == "app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("instructor_dashboard"))
            elif user.user_type == "4":
                if modulename == "app.MEMBERS_VIEWS" or modulename == "django.views.static":
                    pass
                elif modulename == "app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("member_dashboard"))

            elif user.user_type == "5":
                if modulename == "app.TRAINING_VIEWS" or modulename == "django.views.static":
                    pass
                elif modulename == "app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("member_dashboard"))
            # else:
            #     return HttpResponseRedirect(reverse("member_login"))

        # else:
        #     if request.path == reverse("member_login") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="app.MEMBERS_VIEWS":
        #         pass
        #     else:
        #         return HttpResponseRedirect(reverse("member_login"))