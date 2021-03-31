from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from store.models.products import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View

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

                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                print(request.session.get('email'))
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

def logout(request):
    request.session.clear()
    return redirect('login')