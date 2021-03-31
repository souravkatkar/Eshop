from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.products import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View



class Index(View):
    def get(self,request):
        products = None
        cart = request.session.get('cart')
        email = request.session.get('email')
        if not email:
            request.session['email'] = None
        if not cart:
            request.session['cart'] = {}

        categories = Category.get_all_categories()
        
        data ={}

        category_id = request.GET.get('category')
        request.session['category'] = category_id
        
        if category_id:
            products = Product.get_all_products_by_categoryid(category_id)

        else:
            products = Product.get_all_products()
            
        
        print(products[0].name,products[0].price,products[0].image)
        data['products'] = products
        data['categories'] = categories
        return render(request,'index.html',data)

    def post(self,request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <=1 :
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1    
        else:
            cart ={}
            cart[product] = 1
        
        request.session['cart'] = cart
        print(request.session['email'],request.session['cart'],request.session['category'])

        categories = Category.get_all_categories()
        
        data ={}

        category_id = request.session['category']
        
        if category_id:
            products = Product.get_all_products_by_categoryid(category_id)

        else:
            products = Product.get_all_products()
            
        

        data['products'] = products
        data['categories'] = categories

        return render(request,'index.html',data)



        

