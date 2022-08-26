from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save

# Create your models here.

# Models for Sliders
class Slider(models.Model):

    image = models.ImageField(upload_to='sliders')
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name

# Models for Banners1
class Banner1(models.Model):
    image=models.ImageField(upload_to='banners1')
    deal = models.CharField(max_length=100)
    quote = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.quote

# Models for Banners2
class Banner2(models.Model):
    image=models.ImageField(upload_to='banners2')
    deal = models.CharField(max_length=100)
    quote = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.quote

# Models for Timer
class Timer(models.Model):
    datetime=models.CharField(max_length=100)
    def __str__(self):
        return self.datetime

# Models for Main Categories
class Main_Categories(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

# Models for Categories
class Categories(models.Model):
    main_categories=models.ForeignKey(Main_Categories,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.main_categories.name + " : " + self.name 

# Models for Sub_Categories
class Sub_Categories(models.Model):
    categories=models.ForeignKey(Categories,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.categories.main_categories.name + " : " + self.categories.name +  " : " + self.name 

#Models for Section

class Section(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

# Models for Product
class Product(models.Model):
    
    total_quantity=models.IntegerField()
    a_quantity=models.IntegerField()
    featured_image= models.ImageField(upload_to='featured')
    product_name=models.CharField(max_length=200)
    price=models.IntegerField()
    discount=models.IntegerField()
    tax=models.IntegerField(null=True)
    packing_charge=models.IntegerField(null=True)
    product_information = RichTextField()
    model_name=models.CharField(max_length=100)
    categories=models.ForeignKey(Categories,on_delete=models.CASCADE)
    tags=models.CharField(max_length=200)
    description = RichTextField()
    section=models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("product_deatil", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

#  Models for Coupon Code
class Coupon_Code(models.Model):
    code= models.CharField(max_length=100)
    discount=models.IntegerField()

def __str__(self):
     return self.code


# Models for Product Image 

class Product_Image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')
       

# Models for Additional_Information 

class Additional_Information(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    specification=models.CharField(max_length=200)
    detail=models.CharField(max_length=500)