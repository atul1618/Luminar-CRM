from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count,Sum



from .models import Enquiry
from .forms import *
# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from datetime import date


class EnquiryList(ListView):
    model=Enquiry
    paginate_by = 5
    template_name="enq/enq_list.html"
    ordering = ['-enquirydate']
    # obj=Enquiry.objects.all()
    # context={}
    # context['lstenq']=obj
    # return render(request,template_name,context)


class CreateEnquiry(CreateView):
    model=Enquiry
    form_class =EnquiryForm
    template_name = "enq/enq_form.html"
    success_url = reverse_lazy('listenq')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ViewEnquiry(DetailView):
    model = Enquiry
    template_name = "enq/enq_view.html"
    context_object_name = "details"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ViewEnquiry, self).dispatch(request,*args,**kwargs)

class UpdateEnquiry(UpdateView):
    model = Enquiry
    form_class = EnquiryUpdateForm
    template_name="enq/enq_update.html"
    success_url = reverse_lazy('listenq')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateEnquiry, self).dispatch(request,*args,**kwargs)

class DeleteEnquiry(DeleteView):
    model = Enquiry
    template_name = "enq/enq_delete.html"
    success_url = reverse_lazy('listenq')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteEnquiry, self).dispatch(request,*args,**kwargs)

class FollowUp(TemplateView):
    model=Enquiry
    template_name = "enq/enq-followups.html"

    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super(FollowUp, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Enquiry.objects.filter(followup_date=date.today(),status='1')
    def get(self, request, *args, **kwargs):
        context={}
        context['enquiries']=self.get_queryset()
        return render(request,self.template_name,context)





# class FollowUpDetail(UpdateView):
#     model = Enquiry
#     form_class = EnquiryUpdateForm
#     template_name = "enq/followupdetail.html"
#     success_url = reverse_lazy('listenq')

class FollowUpDetail(TemplateView):
    model=Enquiry
    form_class=EnquiryUpdateForm
    template_name = "enq/followupdetail.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(FollowUpDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Enquiry.objects.get(enquiryid=id)
        form=self.form_class(instance=qs)
        context={}
        context['form']=form
        context['id']=id
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Enquiry.objects.get(enquiryid=id)
        form = self.form_class(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            return redirect('followup')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)


# View all followups based on user selected date

class ViewFollowUp(TemplateView):
    model=Enquiry
    form_class = FollowUpViewForm
    template_name = "enq/viewfollowupsearch.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(ViewFollowUp, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
       form=self.form_class(request.POST)
       if form.is_valid():
           dte=form.cleaned_data['followup_date']
           print(dte)
           qs=Enquiry.objects.filter(followup_date=dte,status='1')
           if(qs):
               print(qs)
               context={}
               context['item']=qs
               template_name="enq/viewfollowupall.html"
               return render(request,template_name,context)
           else:
               form = self.form_class(request.POST)
               context = {}
               context['form'] = form
               return render(request, self.template_name, context)


       else:
           form=self.form_class(request.POST)
           context={}
           context['form']=form
           return render(request,self.template_name,context)

class StudentInfoFollow(TemplateView):
    model=Enquiry
    template_name = "enq/studentinfo_followup.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(StudentInfoFollow, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Enquiry.objects.filter(enquiryid=id)
        context={}
        context['info']=qs
        return render(request,self.template_name,context)

class PendingFollowUp(TemplateView):
    model=Enquiry
    template_name = "enq/pendingfollowups.html"
    form_class=PendingFollowUpFrm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(PendingFollowUp, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            date1 = form.cleaned_data['followup_date']
            print(date1)
            date2 = form.cleaned_data['enquirydate']
            print(date2)
            qs=Enquiry.objects.filter(followup_date__gte=date1,followup_date__lte=date2,status='1')
            if (qs):
                print(qs)
                context = {}
                context['item'] = qs
                template_name = "enq/viewfollowupall.html"
                return render(request, template_name, context)
            else:
                form = self.form_class(request.POST)
                context = {}
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)



# Course creation

class CourseCreation(TemplateView):
    model=Course
    form_class=CourseForm
    template_name = "course/coursecreation.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(CourseCreation, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=self.form_class
        qs = Course.objects.all()
        context={}
        context['form']=form
        context['courselist']=qs
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            print("Saved")
            return redirect('createcourse')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)
        
        
class CourseUpdation(TemplateView):
    model=Course
    form_class=CourseUpdateForm
    template_name = "course/courseupdate.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(CourseUpdation, self).dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Course.objects.get(id=id)
        form=self.form_class(instance=qs)
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Course.objects.get(id=id)
        form = self.form_class(request.POST,instance=qs)
        print(id)
        print(qs)
        if form.is_valid():
            form.save()
            return redirect('createcourse')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)

class CourseDelete(TemplateView):
    model=Course
    template_name = "course/coursedelete.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(CourseDelete, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        print(id)
        qs=Course.objects.get(id=id).delete()
        context={}
        context['delobj']=qs
        return redirect('createcourse')


class BatchCreation(TemplateView):
    model=Batch
    template_name = "batch/batchcreate.html"
    form_class=BatchForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(BatchCreation, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form=self.form_class
        qs = Batch.objects.all()
        context = {}
        context['batch'] = qs
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createbatch')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)


class BatchUpdate(TemplateView):
    model=Batch
    template_name = "batch/batchupdate.html"
    form_class=BatchUpdateForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(BatchUpdate, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        b_id=self.kwargs.get('pk')
        qs=Batch.objects.get(id=b_id)
        form=self.form_class(instance=qs)
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):

        b_id = self.kwargs.get('pk')
        qs = Batch.objects.get(id=b_id)
        form = self.form_class(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            return redirect('createbatch')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)

class BatchDelete(TemplateView):
    model=Batch
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(BatchDelete, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        b_id=self.kwargs.get('pk')
        qs=Batch.objects.get(id=b_id).delete()
        context={}
        context['delbatch']=qs
        return redirect('createbatch')

class NewAdmission(TemplateView):
    model=Admission
    template_name = "admission/new_admission.html"
    form_class=NewAdmissionForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(NewAdmission, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Enquiry.objects.get(enquiryid=id)
        name=qs.studentname
        batchcode=qs.batch
        form=self.form_class(initial={'enquiryid':id,'studentname':name,'batchcode':batchcode})
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            print("Valid")
            id=self.kwargs.get('pk')
            qs=Enquiry.objects.get(enquiryid=id)
            qs.status='2'
            qs.save()
            admission_no=form.cleaned_data['admission_no']
            form.save()
            # request.method='GET'
            # return StudentPayment.as_view()(self.request, *args, **kwargs)
            return redirect('payment',pk=admission_no)
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)


class StudentPayment(TemplateView):
    model=Payment
    template_name = "admission/payment.html"
    form_class=PaymentForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(StudentPayment, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Admission.objects.get(admission_no=id)
        print(qs)
        enqid=qs.enquiryid
        print("Enq Id:",enqid)
        fees=qs.coursefees
        batch=qs.batchcode
        print("Batch:",batch)
        print("Fees:",fees)
        qs1=Enquiry.objects.get(enquiryid=enqid)
        from django.db.models import Sum
        # qs2=Payment.objects.filter(admission_no=id).values('amount').annotate(total=Sum('amount'))
        qs2 = Payment.objects.filter(admission_no=id).values('amount').aggregate(total=Sum('amount'))
        print(qs2)
        print(type(qs2))
        print(qs2['total'])
        if(qs2['total']==None):
            remaining = fees
        else:
            remaining = fees - (qs2['total'])

        form=self.form_class(initial={'admission_no':id,'enquiryid':enqid,'batch':batch})
        context={}
        context['remaining']=remaining
        context['info']=qs1
        context['form']=form
        # context={}
        # context['enqid']=id
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            print("Valid")
            id=self.kwargs.get('pk')
            print(id)
            # (Admission id)
            queryset=Admission.objects.get(admission_no=id)
            stdenqid=queryset.enquiryid
            enqqueryset=Enquiry.objects.get(enquiryid=stdenqid)
            if enqqueryset.status=='1':
                enqqueryset.status='2'
                enqqueryset.save()
            else:
                pass
            form.save()
            return redirect('payview',pk=id)
        else:
            form = self.form_class(request.POST)
            context={'form':form}
            return render(request,self.template_name,context)

class StdPayment(TemplateView):
    model=Payment
    template_name = "payments/paymentform.html"
    form_class=StudentPayForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(StdPayment, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            id=form.cleaned_data['admission_no']
            return redirect('payment',pk=id)
        else:
            form = self.form_class(request.POST)
            context={}
            context['form'] = form
            return render(request, self.template_name, context)

@login_required(login_url='accounts/login/')
def paysearch(request):
    searchtag=request.GET['search']
    print(searchtag)
    qs=Admission.objects.filter(studentname__icontains=searchtag)
    searchresults={}
    searchresults['admission']=qs
    searchresults['search']=searchtag
    template_name="search/payment_search.html"
    return render(request,template_name,searchresults)

@login_required(login_url='accounts/login/')
def search(request):
    searchtag=request.GET['search']
    print(searchtag)
    qs=Admission.objects.filter(studentname__icontains=searchtag)
    searchresults={}
    searchresults['admission']=qs
    searchresults['search']=searchtag
    template_name="search/admission_no_search.html"
    return render(request,template_name,searchresults)
    # return HttpResponse("This is search")




class PaymentView(TemplateView):
    model=Payment
    template_name = "payments/paymentview.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        qs=Payment.objects.filter(admission_no=id)
        from django.db.models import Sum
        qs1=Payment.objects.filter(admission_no=id).values('amount').aggregate(total=Sum('amount'))
        qs2=Admission.objects.get(admission_no=id)
        fees=qs2.coursefees
        remaining=fees-qs1['total']
        msg=""
        if remaining==0:
            msg = "Fees fully paid"
        else:
            pass

        context={}
        context['payinfo']=qs
        context['rem_fees']=remaining
        context['msg']=msg
        context['info']=qs2
        return render(request,self.template_name,context)

class PaymentInfo(TemplateView):
    model = Payment
    template_name = "payments/paymentinfo.html"
    form_class = StudentPayForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentInfo, self).dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            id=form.cleaned_data['admission_no']
            return redirect('payview',pk=id)
        else:
            form = self.form_class(request.POST)
            context={}
            context['form'] = form
            return render(request, self.template_name, context)

class Index(TemplateView):
    model=Enquiry
    template_name = "index.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(Index, self).dispatch(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        id=self.kwargs.get('pk')
        print("Id:",id)
        from django.db.models import Count
        qs1=Enquiry.objects.filter(batch__batch_status='1').values('enquiryid').aggregate(enq=Count('enquiryid'))
        qs2=Admission.objects.filter(batchcode__batch_status='1').values('admission_no').aggregate(adm=Count('admission_no'))
        qs3=Enquiry.objects.filter(batch__batch_status='1',status='1').values('enquiryid').aggregate(follow=Count('enquiryid'))
        qs4=Batch.objects.filter(batch_status='1').values('batch_code','batch_date','course__course_name')
        # qs4=Enquiry.objects.filter(batch__batch_status='1').values('batch__batch_code','batch__course__course_name',
        #                                                            'batch__batch_date','batch_id')
        qs5 = Batch.objects.filter(batch_status='2').values('batch_code', 'batch_date','course__course_name').annotate()
        from django.db.models.functions import ExtractMonth

        monthly_earning1=Payment.objects.annotate(m=ExtractMonth('payment_date')).values('m').annotate(total=Sum('amount')).values('total')
        print("Enquiry Count:",qs1)
        print("Admission Count:",qs2)
        print("Call back count:",qs3)
        print("Upcoming:",qs4)
        print("Earnings:",monthly_earning1)
        context={'enqcount':qs1['enq'],'admcount':qs2['adm'],'followcount':qs3['follow'],'upcoming':qs4,'ongoing':qs5,'earning':monthly_earning1}
        return render(request,self.template_name,context)

class IndexDetails(TemplateView):
    model=Enquiry
    template_name = "indexdetails.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(IndexDetails, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        print("ID:",id)
        from django.db.models import Count,Sum
        # >>>>>>>>>>>>>>>To get call back people count <<<<<<<<<<<<<<<<<
        qs1=Enquiry.objects.filter(batch__batch_code=id,status='1').aggregate(call=Count('enquiryid'))

        # >>>>>>>>>>>>>To get admitted people count<<<<<<<<<<<<<<<<<<<
        qs2=Enquiry.objects.filter(batch__batch_code=id,status='2').aggregate(adm=Count('enquiryid'))
        print(qs1)
        print(qs2)
        from django.db.models import Case, When, Value, CharField
         # >>>>>>>>>>>>>>>>>>>>>>> To get batch status <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        choice = dict(Batch._meta.get_field('batch_status').flatchoices)
        print("Choice:",choice)
        whens = [When(batch_status=k, then=Value(v)) for k, v in choice.items()]
        qs3 = Batch.objects.filter(batch_code=id).annotate(status=Case(*whens,output_field=CharField()))\
            .values('batch_code', 'course__course_name', 'batch_date',
                                                         'course__course_duration', 'status')
        print(qs3)
        # >>>>>>>>>>>>>>>>>>To get total enquiries  <<<<<<<<<<<<<<<<<<<<<<<<<
        qs4 = Enquiry.objects.filter(batch__batch_code=id).aggregate(enq=Count('enquiryid'))
        print(qs4)
        # >>>>>>>>>>>>>>>>>>To get cancelled enquires count<<<<<<<<<<<<<<<<<<<
        qs5 = Enquiry.objects.filter(batch__batch_code=id, status='3').aggregate(can=Count('enquiryid'))
        print(qs5)
        # >>>>>>>>>>>>>>>To get total earnings<<<<<<<<<<<<<<<<<<<<<<<<<
        q6=Payment.objects.filter(batch=id).aggregate(income=Sum('amount'))
        print(q6)
        # >>>>>>>>>>>>>>>>>To get enquiry status<<<<<<<<<<<<<<<<<<
        choice_enq=dict(Enquiry._meta.get_field('status').flatchoices)
        print("Choice enq:",choice_enq)
        status_value=[When(status=k, then= Value(v)) for k,v in choice_enq.items()]
        qs7=Enquiry.objects.filter(batch__batch_code=id).annotate(std_status=Case(*status_value,output_field=CharField())).\
            values('enquiryid','studentname','contact','counsellor__counsellor_name','std_status')
        print(qs7)
        qs8=Admission.objects.filter(batchcode__batch_code=id).values('admission_no','studentname','date','coursefees','enquiryid')
        print(qs8)
        context={'batchinfo':qs3,'callback':qs1['call'],'admitted':qs2['adm'],'code':id,'enquiries':qs4['enq'],'cancelcount':qs5['can'],
                 'earnings':q6['income'],'stdinfo':qs7,'adm':qs8}
        return render(request,self.template_name,context)
        # return HttpResponse("Hi")

class AdmView(TemplateView):
    model=Admission
    template_name = "admission/index_admview.html"
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(AdmView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('pk')
        print("Enquiry Id:",id)
        from django.db.models import Case, When, Value, CharField
        choice = dict(Enquiry._meta.get_field('status').flatchoices)
        print("Choice:", choice)
        status_value = [When(status=k, then=Value(v)) for k, v in choice.items()]
        qs=Enquiry.objects.filter(enquiryid=id).annotate(std_status=Case(*status_value,output_field=CharField())).\
            values('studentname','address','qualification','collegename',
                                                       'counsellor__counsellor_name','contact','email','std_status')
        print("Adm View:",qs)
        context={'details':qs}
        return render(request,self.template_name,context)

class BatchReport(TemplateView):
    model=Admission
    template_name = "reports/batchreport_select.html"
    form_class=BatchReportForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(BatchReport, self).dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            batch=form.cleaned_data['batchcode']
            print(batch)
            qs = Admission.objects.filter(batchcode__batch_code=batch).values('batchcode__course__course_name','batchcode__batch_status',
                'batchcode__batch_date','batchcode__batch_code').annotate(expected=Sum('coursefees'), students=Count('admission_no'))
            print(qs)
            from django.db.models import Case, When, Value,CharField
            choice = dict(Batch._meta.get_field('batch_status').flatchoices)
            whens=[When(batch_status=k, then=Value(v)) for k,v in choice.items()]
            # flatchoices gets the value
            print(choice)
            print(type(choice))
            qs1=Batch.objects.filter(batch_code=batch).annotate(status=Case(*whens,output_field=CharField())).\
                values('status')
            print(qs1)
            qs2=Payment.objects.filter(batch=batch).values('amount').aggregate(collected=Sum('amount'))
            print("Collected",qs2)
            qs3=Enquiry.objects.filter(batch=batch).values('batch').annotate(enq=Count('enquiryid'))
            print("Enquiries:",qs3)
            context={}
            context['batch']=qs
            context['batchstatus']=qs1
            context['revenue']=qs2
            context['enquiries']=qs3
            template_name="reports/batchreport.html"
            return render(request,template_name,context)
        else:
            form = self.form_class(request.POST)
            context={}
            context['form']=form
            return render(request,self.template_name,context)





class CreateCounsellor(TemplateView):
    model=Counsellor
    template_name = "counsellor/counsellor_create.html"
    form_class=CounsellorForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCounsellor, self).dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        form=self.form_class
        qs=Counsellor.objects.all()
        context={}
        context['counsellor']=qs
        context['form']=form
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('counsellor_create')
        else:
            form = self.form_class(request.POST)
            context={}
            context['form'] = form
            return render(request, self.template_name, context)

class CounsellorEnquiryReport(TemplateView):
    model=Enquiry
    template_name = "reports/counsellor_enqreport_form.html"
    form_class=CounsellorReportForm
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(CounsellorEnquiryReport, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context['form']=form
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            name=form.cleaned_data['counsellor']
            date1=form.cleaned_data['followup_date']
            date2=form.cleaned_data['enquirydate']
            print(name)
            template_name='reports/counsellorreport.html'
            qs=Enquiry.objects.filter(counsellor=name,enquirydate__gte=date1,enquirydate__lte=date2).values('counsellor__counsellor_name').annotate(enq=Count('enquiryid'))
            qs1 = Enquiry.objects.filter(counsellor=name,status='2',enquirydate__gte=date1,enquirydate__lte=date2).\
                values('counsellor__counsellor_name').annotate(
                enq=Count('enquiryid'))
            print(qs)
            print(qs1)
            context={}
            context['report']=qs
            context['admissions']=qs1
            context['name']=name
            return render(request,template_name,context)
        else:
            form = self.form_class(request.POST)
            context={}
            context['form']=form
            return render(request, self.template_name, context)


def base(request):
    return render(request,'base.html')


class ViewCourses(ListView):
    model=Course
    template_name = "course/viewcourses.html"
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(ViewCourses, self).dispatch(request, *args, **kwargs)


# class ViewAdmissions(TemplateView):
#     model = Admission
#     template_name = "admission/viewadmissions.html"
#
#     def get(self, request, *args, **kwargs):
#         qs=Admission.objects.filter(batchcode__batch_status='1')
#         context={}
#         context['admission']=qs
#         return render(request,self.template_name,context)


class ViewAdmissions(ListView):
    model = Admission
    template_name = "admission/viewadmissions.html"
    context_object_name = "admission"
    paginate_by = 3
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(ViewAdmissions, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Admission.objects.filter(batchcode__batch_status='1')

class ViewAllBatches(ListView):
    model = Batch
    template_name = "batch/all_batches.html"
    context_object_name = "batch_list"
    paginate_by = 2
    
    @method_decorator(login_required)
    
    def dispatch(self, request, *args, **kwargs):
        return super(ViewAllBatches, self).dispatch(request, *args, **kwargs)



