from django.shortcuts import render, Http404

from .models import Product, ProductImage

def home(request):
	products = Product.objects.all()

	stock = {'EXCAVADORA': None,
	 'RETROEXCAVADORA': None,
	 'MOTONIVELADORA': None,
	 'PALACARGADORA': None,
	 'COMPACTADORA': None,
	 'MINICARGADORA': None,
	 'BULLDOZER': None,
	 'MINIEXCAVADORA': None,
	 'GRUA': None,
	 'HAULOTTE': None }

	for key in stock:
		count_stock = Product.objects.filter(machinetype=key).count()
		stock[key] = count_stock

	context = {"products": products, "stock": stock}	
	template ='home.html'
	return render(request, template, context)

def aboutus(request):
	context = locals()
	template ='aboutus.html'
	return render(request, template, context)

def contact(request):
	context = locals()
	template ='contact.html'
	return render(request, template, context)

def list_machines(request, machinetype):
	products = Product.objects.filter(machinetype=machinetype.upper())
	context = {"products": products}	
	template ='products/list_machines.html'
	return render(request, template, context)

def single(request, slug):
	try:
		product = Product.objects.get(slug=slug)		
		images = ProductImage.objects.filter(product=product)
		context = {'product': product, "images": images}
		template = 'products/single.html'	
		return render(request, template, context)
	except:
		raise Http404