from typing import Dict
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html',context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html' ,context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            print("user doesnt exist")
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            print("user exists")
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        print(request)
        url = "https://572470d1.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealers = get_dealers_from_cf(url)
        results = []
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = {"address":dealer_doc.address, "city":dealer_doc.city, "full_name":dealer_doc.full_name,
                                   "id":dealer_doc.id, "lat":dealer_doc.lat, "long":dealer_doc.long,
                                   "short_name":dealer_doc.short_name,
                                   "state":dealer_doc.st, "zip":dealer_doc.zip}
            results.append(dealer_obj)

        context["dealership_list"] = results
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    dealer = {}
    dealer['id'] = dealer_id
    context['dealer'] = dealer

    if request.method == "GET":
        url = "https://572470d1.eu-gb.apigw.appdomain.cloud/api/review"+'/?id='+str(dealer_id)
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url)
        context['reviews'] = reviews
        list_of_reviews = ' '.join([review.review for review in reviews])
        list_of_reviews += ' '.join([review.sentiment for review in reviews])
        # list_of_reviews = str(reviews) 
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    dealer = {}
    dealer['id'] = dealer_id
    context['dealer'] = dealer

    if request.method == 'GET':
        context["cars"] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            url = "https://572470d1.eu-gb.apigw.appdomain.cloud/api/review/"
            review = {}
            car = CarModel.objects.get(pk= request.POST['car'])
            review["time"] = datetime.utcnow().isoformat()
            review["id"] = 1337
            review["name"] = request.user.first_name+ " " + request.user.last_name
            review["dealership"] = dealer_id
            review["car_make"] = car.carMake.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            review["purchase_date"] = request.POST['purchasedate']
            review["review"] = request.POST['content']
            review["purchase"] = request.POST['purchasecheck'] == 'on'
            json_payload = {}
            json_payload["review"] = review
            post_request(url, json_payload, id=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        else:
            context['message'] = "Log in before posting a Review"
            return render(request, 'djangoapp/add_review.html', context)
    #... # Do something for anonymous users.

