from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,TemplateView,ListView,DetailView,UpdateView,DeleteView,RedirectView
from django.urls import reverse_lazy,reverse
from app.models import Product,Order,ProductOrder,AddCart
from django.contrib import messages
from django.http import Http404,response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework import viewsets 
from app.api.serializers import AccountSerializer
from django.conf import settings
import stripe
from datetime import datetime
stripe.api_key='sk_test_51Hwk3xHnmBUEg3J6hroVbskTMYEaemtSaXyXNXrdw2tngochUvV3QTSqUZ7IIGJJPKJeRM3HzK5sAQkz3a96Ir8s00w0fx58BV'

class TemplateMyOrderListView(TemplateView):
	template_name='app/myorder.html'
	print("piyushgarg")


class ProductList(ListView):
	model = Product
	

# def ProductList(request):
# 	product=Product.objects.all()
	
# 	return response(product)






def ProductSearch(request):
	if request.method=='GET':

		query=request.GET.get('search')
		product_list=Product.objects.filter(product_name__contains=query)

		return render(request,'app/product_list.html',{'product_list':product_list})

	else:
		return redirect('app:listnotfound')




class ProductDetail(DetailView):
	model=Product


def AddToCart(request,pk):

	product=get_object_or_404(Product,pk=pk)
	print(product)
	try:
		AddCart.objects.create(user=request.user,product=product)

	except:
		messages.warning(request,'Please Login')
		redirect('account:login')

	else:
		messages.success(request,'your paroduct is saved in cart')

	return redirect('app:cartlist')




class OrderView(CreateView,LoginRequiredMixin):
	model=Order
	fields=('order_date',)
	
	def form_valid(self,form,*args,**kwargs):
		self.object=form.save(commit=False)
		self.object.user=self.request.user
		
		self.object.save()
		product=get_object_or_404(Product,slug=self.kwargs['slug'])


		try:
			ProductOrder.objects.create(product=product,order=self.object)
			messages.success(self.request,'you are the member of the group')
		except IntegrityError :
			messages.warning(self.request,'warning already')

		
		return super().form_valid(form,*args,**kwargs)


class OrderCancel(RedirectView,LoginRequiredMixin):

	def get_redirect_url(self,*args,**kwargs):
		return reverse('app:myorder')


	def get(self,request,*args,**kwargs):
		
		o=Order.objects.get(pk=self.kwargs['pk'])
		
		ProductOrder.objects.filter(
		order=self.kwargs.get('pk'),
		product__slug=self.kwargs.get('slug')
		).delete()
		o.delete()
		return super().get(request,*args,**kwargs)


class OrderRemoveCart(RedirectView,LoginRequiredMixin):

	def get_redirect_url(self,*args,**kwargs):
		return redirect('app:cartlist')


	def get(self,request,*args,**kwargs):
		

		AddCart.objects.filter(
		user=self.request.user,
		product__slug=self.kwargs.get('slug'),
		
		).delete()


		
		return redirect('app:cartlist')



class TemplateCartListView(TemplateView):
	template_name='app/product_cart.html'


def CheckOutView(request,slug):
	
	product=get_object_or_404(Product,slug=slug)
	context={'slug':slug,'product':product}

	return render(request,'app/checkout.html',context)


@login_required
def SuccessPage(request,slug):

	

	order=Order.objects.create(user=request.user,order_date=datetime.now())
	product=get_object_or_404(Product,slug=slug)
	
	customer=stripe.Customer.create(
		email=request.user.email,
		name=request.POST['name'],
		source=request.POST['stripeToken'],
	)
	charge=stripe.Charge.create(
		customer=customer,
		amount=product.product_price,
		currency='inr',
		description=product.product_name,
		
	)
	if charge:{

		ProductOrder.objects.create(product=product,order=order)
	}

	context ={'product':product,}
	print("mychanges")
	print("secondchanges")
	return render(request,'app/successpage.html',context)
