from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class EnquiryForm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['studentname','address','qualification','collegename','course','batch','counsellor','source','contact','email','enquirydate','followup_date','status']
        widgets={
            'studentname':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={"rows":3,"col":5}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'collegename':forms.TextInput(attrs={'class':'form-control'}),
            'course':forms.Select(attrs={'class':'form-control'}),
            'batch':forms.Select(attrs={'class':'form-control'}),
            'counsellor':forms.Select(attrs={'class':'form-control'}),
            'source':forms.TextInput(attrs={'class':'form-control'}),
            'contact':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'enquirydate':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'followup_date':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status':forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        print("inside clean")


class EnquiryUpdateForm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['studentname','address','qualification','collegename','course','batch','counsellor','source','contact','email','enquirydate','followup_date','status']
        widgets={
            'studentname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={"rows": 3, "col": 5}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'collegename': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'counsellor': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'enquirydate': forms.SelectDateWidget(),
            # 'followup_date': forms.SelectDateWidget(),
            'enquirydate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        print("inside clean")


class CourseForm(ModelForm):
    class Meta:
        model=Course
        fields=['course_name','course_duration']
        widgets={
            'course_name':forms.TextInput(attrs={'class':'form-control'}),
            'course_duration':forms.TextInput(attrs={'class':'form-control'}),

        }

    def clean(self):
        print("inside clean")



class BatchForm(ModelForm):
    class Meta:
        model=Batch
        fields=['batch_code','course','batch_date','batch_status']

        widgets={
            'batch_code':forms.TextInput(attrs={'class':'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_date': forms.DateInput(format=('%y/%m/%d'),attrs={'class':'form-control','type':'date'}),
            'batch_status':forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        code=cleaned_data.get('batch_code')
        print("Code:",code)
        qs=Batch.objects.filter(batch_code=code)
        if qs:
            msg="Batch code already exists"
            self.add_error("batch_code",msg)


class CourseUpdateForm(ModelForm):
    class Meta:
        model=Course
        fields = ['course_name','course_duration']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_duration':forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        print("inside clean")

class BatchUpdateForm(ModelForm):
    class Meta:
        model=Batch
        fields=['batch_code','course','batch_date','batch_status']
        widgets={
            'batch_code':forms.TextInput(attrs={'class':'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'batch_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        print("inside clean")


class FollowUpViewForm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['followup_date']
        widgets={
            'followup_date':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        date=cleaned_data.get('followup_date')
        qs=Enquiry.objects.filter(followup_date=date,status='1')
        if qs:
            print("Found")
        else:
            msg="No Follow Ups on selected date"
            self.add_error("followup_date",msg)
            print("error")

class PendingFollowUpFrm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['enquirydate','followup_date']
        widgets={
            'enquirydate':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'followup_date':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        date1 = cleaned_data.get('followup_date')
        date2 = cleaned_data.get('enquirydate')
        qs = Enquiry.objects.filter(followup_date__gte=date1, followup_date__lte=date2, status='1')
        print('qs')
        if (qs):
            print("Found")
        else:
            print("error")
            msg="No followUps On Selected Dates"
            self.add_error("enquirydate",msg)
            print("passed")





class NewAdmissionForm(ModelForm):
    class Meta:
        model=Admission
        exclude=['date']
        widgets={
            'admission_no':forms.TextInput(attrs={'class':'form-control'}),
            'studentname':forms.TextInput(attrs={'class':'form-control'}),
            'enquiryid':forms.HiddenInput(),
            'coursefees':forms.TextInput(attrs={'class':'form-control'}),
            'batchcode':forms.Select(attrs={'class':'form-control'})
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        ad_no=cleaned_data.get('admission_no')
        enq_no=cleaned_data.get('enquiryid')
        print("Enquiry Id:",enq_no)
        print("Admission No:",ad_no)
        qs=Admission.objects.filter(admission_no=ad_no)
        if qs:
            msg="Admission Number exists"
            self.add_error('admission_no',msg)
            print("Error")
        else:
            print("Passed")



class PaymentForm(ModelForm):
    class Meta:
        model=Payment
        exclude=['payment_date']
        widgets={
            'admission_no':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'enquiryid':forms.HiddenInput(),
            'batch':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        enq=cleaned_data.get('enquiryid')
        print("Enquiry Id Payment Form:",enq)
        pay=cleaned_data.get('amount')
        print(type(pay))
        print("Amount:",pay)
        if pay<500:
            msg="Payment should be above 500"
            self.add_error('amount',msg)
        else:
            print("Payment Ok")



class StudentPayForm(ModelForm):
    class Meta:
        model=Payment
        fields=['admission_no']
        widgets={
            'admission_no':forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        adm_no=cleaned_data.get('admission_no')
        print(adm_no)
        qs=Admission.objects.filter(admission_no=adm_no)
        if qs:
            print("Valid admission no")
        else:
            msg="Invalid admission no"
            self.add_error('admission_no',msg)
            print("Found")


class BatchReportForm(ModelForm):
    class Meta:
        model=Admission
        fields=['batchcode']
        widgets={
            'batchcode':forms.Select(attrs={'class':'form-control'})
        }

    def clean(self):
        print("inside clean")

class CounsellorForm(ModelForm):
    class Meta:
        model=Counsellor
        fields=['counsellor_name']
        widgets={
            'counsellor_name':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        print("inside clean")

class CounsellorReportForm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['counsellor','enquirydate','followup_date']
        widgets = {
            'counsellor': forms.Select(attrs={'class': 'form-control'}),
            'enquirydate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def clean(self):
        print("inside clean")
        cleaned_data=super().clean()
        enqdate=cleaned_data.get('enquirydate')
        followup_date=cleaned_data.get('followup_date')
        print("Enq:",enqdate)
        print("Followup:",followup_date)
