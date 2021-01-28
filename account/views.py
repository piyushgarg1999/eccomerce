from django.shortcuts import render,get_object_or_404,redirect
from account.forms import Signup
from django.views.generic import CreateView,TemplateView,ListView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.

class Registerview(CreateView):
	form_class=Signup
	template_name='account/register.html'
	success_url=reverse_lazy('account:login')
	
# class TemplateTestView(LoginRequiredMixin,ListView):
# 	model = FoodItem
# 	template_name='food/food_list.html'
	
class TemplateTestView(TemplateView):
	template_name='account/test.html'

class LogoutView(TemplateView):
	template_name='account/afterlogout.html'

# Create your views here.

class ProfileUser(TemplateView):
	template_name='account/profile_form.html'


def Email_Massage(request):
	subject=request.POST.get('subject')
	message=get_template('account/mail.html').render()
	to=request.POST.get('email')
	# file=request.FILES['file1']


	email=EmailMessage(subject,message,settings.EMAIL_HOST_USER,[to],reply_to=['gargpiyush363@gmail.com'])
	email.content_subtype='html'
	# email.attach(file.name,file.read(),file.content_type)
	email.send()

	return render(request,'account/mail_sender.html')