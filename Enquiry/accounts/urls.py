from django.urls import  path
from .views import UserReg,UserLogin,userlogout


urlpatterns=[
    path('login/',UserLogin.as_view(),name='login'),
    path('register',UserReg.as_view(),name='userreg'),
    path('logout',userlogout,name='logout'),
]