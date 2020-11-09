"""Enquiry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from studentenquiry.views import *

urlpatterns = [
    # path('',index,name='index'),
    path('base',base,name='base'),
    path('',Index.as_view(),name='index'),
    path('listenq',EnquiryList.as_view(),name='listenq'),
    path('createenq',CreateEnquiry.as_view(),name='createenq'),
    path('viewenq/<str:pk>',ViewEnquiry.as_view(),name='viewenq'),
    path('updateenq/<str:pk>',UpdateEnquiry.as_view(),name='updateenq'),
    path('deleteenq/<str:pk>',DeleteEnquiry.as_view(),name='deleteenq'),
    path('followup',FollowUp.as_view(),name='followup'),
    path('followupdetail/<str:pk>',FollowUpDetail.as_view(),name='followupdetail'),
    path('viewfollowup',ViewFollowUp.as_view(),name='viewfollowup'),
    path('pendingfollowup',PendingFollowUp.as_view(),name='pendingfollowup'),
    path('viewinfo/<str:pk>',StudentInfoFollow.as_view(),name='viewinfo'),
    path('indexdetails/<str:pk>',IndexDetails.as_view(),name='indexdetails'),
    path('createcounsellor',CreateCounsellor.as_view(),name='counsellor_create'),
    path('viewcourses',ViewCourses.as_view(),name='viewcourses'),
    path('newadmissions',ViewAdmissions.as_view(),name='new_admissions'),
    path('viewbatches',ViewAllBatches.as_view(),name='view_all_batches'),
    path('index_adm/<str:pk>',AdmView.as_view(),name='index_admdetails'),

#     course urls
    path('createcourse',CourseCreation.as_view(),name='createcourse'),
    path('courseupdate/<int:pk>',CourseUpdation.as_view(),name='courseupdate'),
    path('deletecourse/<int:pk>',CourseDelete.as_view(),name='deletecourse'),


#     batch urls
    path('createbatch',BatchCreation.as_view(),name='createbatch'),
    path('updatebatch/<int:pk>',BatchUpdate.as_view(),name='updatebatch'),
    path('deletebatch/<int:pk>',BatchDelete.as_view(),name='deletebatch'),


# admission
    path('newadmission/<str:pk>',NewAdmission.as_view(),name='newadmission'),
    path('payment/<str:pk>',StudentPayment.as_view(),name='payment'),
    path('studentpay',StdPayment.as_view(),name='studentpay'),
    path('payview/<str:pk>',PaymentView.as_view(),name='payview'),
    path('payinfo',PaymentInfo.as_view(),name='payinfo'),

    #>>>>>>>>>>>>reports>>>>>>>>>>>>>>>>>>>>>>>
    path('report',BatchReport.as_view(),name='report'),
    path('counslr_report',CounsellorEnquiryReport.as_view(),name='counslr_enqreport'),

#     >>>>>>>>>>Search<<<<<<<<<<<<<
    path('search',search,name='search'),
    path('paysearch',paysearch,name='paysearch'),
]
