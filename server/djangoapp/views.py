from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')



# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        password = request.POST["psw"]
        user = User.objects.create_user(username=username,password=password)
        user.firstname=firstname
        user.lastname=lastname
        user.save()
        auth = authenticate(username=username, password=password)
        login(request, auth)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://027a0ab5.us-east.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://027a0ab5.us-east.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        reviews_list = ', '.join([review.sentiment for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(reviews_list)

# Create a `add_review` view to submit a review
def add_review(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            url = "https://027a0ab5.us-east.apigw.appdomain.cloud/api/review"
            review = {"name":"Abdallah Alyamni",
                      "dealership":3,
                      "review":"This is a great car dealer",
                      "purchase":False,
                      "another":"field",
                      "purchase_date":"02/16/2021",
                      "car_make":"Audi",
                      "car_model":"Car",
                      "car_year": 2021
                      }
            json_payload = {}
            json_payload["review"] = review
            response = post_request(url,json_payload)
            # Concat all dealer's short name
            # reviews_list = ', '.join([review.sentiment for review in reviews])
            # Return a list of dealer short name
            return HttpResponse(str(response))
        return HttpResponse("not authenticated")
    return HttpResponse("this is get request")

