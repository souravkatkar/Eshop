from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.products import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View

# Create your views here.
def index(request):

    products = None

    categories = Category.get_all_categories()
    
    data ={}

    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.get_all_products_by_categoryid(category_id)

    else:
        products = Product.get_all_products()
    

    data['products'] = products
    data['categories'] = categories
    return render(request,'index.html',data)


class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
        
    def post(self,request):
        postData = request.POST
        firstName = postData.get('firstName')
        lastName = postData.get('lastName')
        email = postData.get('email')
        password = postData.get('password')

        customer = Customer(firstName = firstName, lastName = lastName,email = email,password = password)

        value = {
            'firstName' : firstName,
            'lastName' : lastName,
            'email' : email
        }
        
        error_message = self.validateCustomer(customer)
        
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')

        else:
            data = {
            'error' : error_message,
            'values': value
            }
        return render(request,'signup.html',data)


    def validateCustomer(self,customer):
        error_message = None
        if len(customer.firstName) < 4:
            error_message = "First Name Should be at least 4 letters long!!"
                
        elif len(customer.lastName) < 4:
            error_message = "Last Name Should be at least 4 letters long!!"
                
        elif len(customer.password) < 6:
            error_message = "Password Should be at least 6 letters long!!"

        elif customer.isExists():
            error_message = "Email address already registered !!"

        return error_message

  

class Login(View):

    def get(self,request):
        return render(request,'login.html')


    def post(self,request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')
    

        customer = Customer.get_by_email(email)
    
        error_message = None

        if customer:
            flag = check_password(password,customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = "Password incorrect!!"
                value = {
                    'email' : email
                }
                data = {
                    'error' : error_message,
                    'values' : value
                }
                return render(request,'login.html',data)
                            
        else:
            error_message = "Invalid Email ID!!"
            return render(request,'login.html',{'error':error_message})


        
