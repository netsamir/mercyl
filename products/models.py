from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Product(models.Model):
	PRODUCT_TYPE = (
		('EXCAVADORA', 'EXCAVADORA'),
		('RETROEXCAVADORA', 'RETROEXCAVADORA'),
		('MOTONIVELADORA', 'MOTONIVELADORA'),
		('PALACARGADORA', 'PALACARGADORA'),
		('COMPACTADORA', 'COMPACTADORA'),
		('MINICARGADORA', 'MINICARGADORA'),
		('BULLDOZER', 'BULLDOZER'),
		('MINIEXCAVADORA', 'MINIEXCAVADORA'),
		('GRUA', 'GRUA'),
		('HAULOTTE','HAULOTTE'),
    )
	title = models.CharField(max_length=120)
	machinetype = models.CharField(max_length=120, choices=PRODUCT_TYPE)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=10, default=35000.99)
	sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
	year = models.DecimalField(decimal_places=0, max_digits=10, null=True, blank=True)
	hours = models.DecimalField(decimal_places=0, max_digits=10, null=True, blank=True)
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

	class Meta:
		unique_together = ('title','slug')	
	
	def get_price(self):
		return self.price

	def get_absolute_url(self):
		return reverse("single", kwargs={"slug": self.slug})
	

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.FileField(upload_to='products/images/')
	featured = models.BooleanField(default=False)
        thumbnail = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.product.title
