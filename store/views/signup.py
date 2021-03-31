from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.products import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View

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
            request.session['customer'] = customer.id
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

  