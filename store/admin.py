from django.contrib import admin
from .models.category import Category
from .models.products import Product
from .models.customer import Customer

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Category,AdminCategory)
admin.site.register(Product,AdminProduct)
admin.site.register(Customer)