from django.contrib import admin
from .models import *

class Product_ImageInline(admin.TabularInline):
    model = Product_Image

class Additional_InformationInline(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = [Product_ImageInline,Additional_InformationInline]
    list_display = ('product_name','categories','section')
    list_editable= ('categories','section')


# Register your models here.
admin.site.register(Slider) 
admin.site.register(Banner1)
admin.site.register(Banner2)
admin.site.register(Timer)
admin.site.register(Main_Categories)
admin.site.register(Categories)
admin.site.register(Sub_Categories)
admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Coupon_Code)





