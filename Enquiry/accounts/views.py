from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .forms import UserRegForm
from django.contrib.auth import login,logout,authenticate
# Create your views here.

class UserReg(TemplateView):
    model=User
    template_name = "user_register.html"
    form_class=UserRegForm

    def get(self, request, *args, **kwargs):
        context={}
        context['form']=self.form_class
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            print("Form Validated")
            return redirect('login')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)

class UserLogin(TemplateView):
    model=User
    template_name = "userlogin.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=uname,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            context={}
            message="Incorrect username or password"
            context['message']=message
            return render(request, self.template_name,context)


def userlogout(request):
    logout(request)
    return redirect('login')
