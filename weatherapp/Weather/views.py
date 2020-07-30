from django.shortcuts import render, HttpResponse, redirect
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
from . models import City, Review, Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=b513d3fef5ac1630c33c40a66d8ec749'
    if request.method == "POST":
        city_name = request.POST['city_name']
        city = City(city_name=city_name)
        ecc = City.objects.filter(city_name=city_name).count()
        if ecc == 0:
            response = requests.get(url.format(city)).json()
            if response['cod'] == 200:
                city.save()
            else:
                messages.warning(request, "City does not exist in api data")
        else:
            messages.warning(request, "City already exists in database")


    cities = City.objects.all()
    weather_data = []
    for city in cities:
        response = requests.get(url.format(city)).json()
        print(response)
        city_weather = {
          'cityn': city,
          'temprature': int(response['main']['temp'] - 274),
           'description': response['weather'][0]['description'],
           'icon': response['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    params = {'weather_data': weather_data}
    return render(request, "Weather/index.html", params)



def about(request):
    if request.method == "POST":
        name1 = request.POST['name1']
        email1 = request.POST['email1']
        phone1 = request.POST['phone1']
        review = request.POST['review']

        review = Review(rname=name1, remail=email1, rphone=phone1, rreview=review)
        review.save()
        messages.success(request, "Your review is submitted")

    return render(request, 'Weather/about.html')


def contact(request):
    if request.user.is_authenticated:
      if request.method == "POST":
        name2 = request.POST['name2']
        email2 = request.POST['email2']
        phone2 = request.POST['phone2']
        query = request.POST['query']
        contact = Contact(cname=name2, cemail=email2, cphone=phone2, cquery=query)
        contact.save()
        messages.success(request, "Your query is submitted. Our team will contact you soon !")

      return render(request, 'Weather/contact.html')
    else:
        messages.warning(request, "Kindly Log-In To Contact Us")
        return redirect('/')





def handleSignUp(request):
    if request.method == "POST":
        email1 = request.POST['email1']
        username = request.POST['username1']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            if username.isalnum == True:
              myuser = User.objects.create_user(username, email1, pass1)
              myuser.save()
              messages.success(request, "You are Signed-Up")
              return redirect('/')
            else:
                messages.warning(request,"Username should be alpha-numeric only !")
                return redirect('/')
        else:
            messages.warning(request, "Passwords did not match !")
            return redirect('/')
    else:
        return HttpResponse('404-Not Found')





def handleLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "You are logged in !")
        return redirect('/')
    else:
        messages.error(request, "Invalid Credential")

def handleLogout(request):
    logout(request)
    messages.success(request, "You are Logged Out !")
    return redirect('/')


def delete_city(request, cityn):
    City.objects.get(city_name=cityn).delete()
    messages.warning(request, "City has been succesfully removed")
    return redirect('/')


