# import email
import email
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.backends import ModelBackend

from app.models import CustomUser

class EmailBackEnd(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        # print(username)
        try:

            user=CustomUser.objects.get(adhaar=username)
        # print(user.password,check_password(password,user.password),make_password(password))
       
            if user.check_password(password):
                return user
        except:
            pass

        # UserModel=get_user_model()
        # try:
        #     user=UserModel.objects.get(email=username)
        # except UserModel.DoesNotExist:
        #     return None
        # else:
        #     if user.check_password(password):
        #         return user
        # return None