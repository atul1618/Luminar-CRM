from django.db import models
from datetime import date
import uuid

# Create your models here.
# Enquiry Id
# Student name,Qualification,College name,Contact No,Email id,Follow Up Date
# Course
# Address,Status(callback,admitted,cancel)
# Enquiry date


class Course(models.Model):
    course_name=models.CharField(max_length=50,unique=True)
    course_duration=models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class  Batch(models.Model):
    batch_code=models.CharField(max_length=50,unique=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_date=models.DateField(default=date.today())
    action=(
        ('1','Yet to begin'),
        ('2','Ongoing'),
        ('3','Completed')
    )
    batch_status=models.CharField(max_length=30,choices=action)

    class Meta:
        ordering=['-batch_date']

    def __str__(self):
        return self.batch_code


class Counsellor(models.Model):
    counsellor_name = models.CharField(max_length=120)

    def __str__(self):
        return self.counsellor_name


class Enquiry(models.Model):
    enquiryid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # enquiryid=models.IntegerField()
    studentname=models.CharField(max_length=100)
    address=models.TextField()
    qualification=models.CharField(max_length=50)
    collegename=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    counsellor=models.ForeignKey(Counsellor,on_delete=models.CASCADE)
    source=models.CharField(max_length=100)
    contact=models.IntegerField()
    email=models.EmailField(unique=True)
    enquirydate=models.DateField(default=date.today())
    followup_date=models.DateField()
    action=(
        ('1','Call_back'),
        ('2','Admitted'),
        ('3','Cancel')
    )
    status=models.CharField(max_length=20,choices=action)

    def __str__(self):
        return str(self.enquiryid)

class Admission(models.Model):
    admission_no=models.CharField(max_length=50,unique=True)
    studentname=models.CharField(max_length=50)
    enquiryid=models.CharField(max_length=50)
    coursefees=models.IntegerField()
    batchcode=models.ForeignKey(Batch,on_delete=models.CASCADE)
    date=models.DateField(default=date.today())

    def __str__(self):
        return self.admission_no

class Payment(models.Model):
    admission_no=models.CharField(max_length=50)
    amount=models.IntegerField()
    batch=models.CharField(max_length=50)
    payment_date=models.DateField(default=date.today())
    enquiryid=models.CharField(max_length=50)

    def __str__(self):
        return self.amount


