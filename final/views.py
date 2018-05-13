from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from final.forms import PropertyForm, PlaceForm
from final.models import Property, Place
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import urllib
import json
import os
import sys

# Zillow API key: X1-ZWz1gebss99q17_4wzn5
# We need to hide the google api key in an OS environment variable since it's sensitive information.
# We access the key using this:
googleApiKey = os.environ.get('GOOGLE_API_KEY')

@csrf_exempt
def home(request):
    if request.user.is_authenticated:
        # get user location so we can center map on them
        ip = request.META.get('REMOTE_ADDR')
        if ip == "127.0.0.1":
            ip = "65.29.183.96"
        c1 = urllib.request.urlopen(
            "http://ip-api.com/json/" + ip)
        c2 = c1.read()
        locationData = json.loads(c2)
        lat = locationData['lat']
        lon = locationData['lon']
        # these will go onto the main screen
        properties = Property.objects.filter(user=request.user.get_username())
        school = Place.objects.filter(type = 'School', user=request.user.get_username())
        job = Place.objects.filter(type = 'Job', user=request.user.get_username())
        other = Place.objects.filter(type = 'Other', user=request.user.get_username())
        return render(request, "home.html", {'properties': properties,
                                             'school': school,
                                             'job': job,
                                             'other': other,
                                             'lat': lat,
                                             'lng': lon,
                                             'googleApiKey': googleApiKey})
    else:
        return redirect("/invalid/")

@csrf_exempt
def add(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "add.html", {'form': PropertyForm(), 'error': 0})
        if request.method == 'POST':
            f = PropertyForm(request.POST)
            if f.is_valid():
                p = f.save(commit=False)
                # find out if user-submitted address works
                address = p.address
                address = address.replace(" ", "%20")
                c1 = urllib.request.urlopen(
                    "https://maps.googleapis.com/maps/api/geocode/json?address="
                    + address + "&key=AIzaSyBeQKOCrIrLMacq-2vXFmbUpUh0GaI-FyM")
                c2 = c1.read()
                addressData = json.loads(c2)
                print(addressData)
                # if this is true then the request was bad
                if addressData['status'] == "ZERO_RESULTS":
                    return render(request, "add.html", {'form': PropertyForm(instance=p), 'error': 1})
                else:
                    address = addressData['results'][0]['formatted_address']
                    # check if this user already added this address
                    if Property.objects.filter(address = address, user=request.user.get_username()).count() > 0:
                        return render(request, "add.html", {'form': PropertyForm(instance=p), 'error': 2})
                    elif Place.objects.filter(address = address, user=request.user.get_username()).count() > 0:
                        return render(request, "add.html", {'form': PropertyForm(instance=p), 'error': 2})
                    else:
                        latitude = addressData['results'][0]['geometry']['location']['lat']
                        longitude = addressData['results'][0]['geometry']['location']['lng']
                        print(latitude)
                        print(longitude)
                        p.user = request.user.get_username()
                        p.latitude = latitude
                        p.longitude = longitude
                        p.address = address
                        p.save()
            return redirect("/home/")
    else:
        return redirect("/invalid/")

@csrf_exempt
def signin(request):
    if request.method == 'GET':
        return render(request, "signin.html", {'form': PropertyForm(), 'error': 0})
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("/home/")
        else:
            return render(request, "signin.html", {'form': PropertyForm(), 'error': 1})
        f = PropertyForm(request.POST)
        if f.is_valid():
            p = f.save(commit=False)
    return render(request, "signin.html", {'form': PropertyForm(instance=p), 'error': 1})

@csrf_exempt
def create(request):
    if request.method == 'GET':
        return render(request, "create.html", {'form': PropertyForm(), 'error': 0})
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if (username == '' or password == '' or email == ''):
            return render(request, "create.html", {'error':1})

        user = User.objects.create_user(username, email, password)
        #user = User.objects.create_user(username, '',password)
        user.save()
    return render(request, "signin.html", {'form': PropertyForm(), 'error': 0})

@csrf_exempt
def addMyPlace(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "addMyPlace.html", {'form': PlaceForm(), 'error': 0})
        if request.method == 'POST':
            f = PlaceForm(request.POST)
            if f.is_valid():
                p = f.save(commit=False)
                # find out if user-submitted address works
                address = p.address
                address = address.replace(" ", "%20")
                c1 = urllib.request.urlopen(
                    "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyBeQKOCrIrLMacq-2vXFmbUpUh0GaI-FyM")
                c2 = c1.read()
                addressData = json.loads(c2)
                # if this is true then the request was bad
                if addressData['status'] == "ZERO_RESULTS":
                    return render(request, "addMyPlace.html", {'form': PlaceForm(instance=p), 'error': 1})
                else:
                    address = addressData['results'][0]['formatted_address']
                    # check if this address is already in the database
                    if Property.objects.filter(address = address, user=request.user.get_username()).count() > 0:
                        return render(request, "addMyPlace.html", {'form': PlaceForm(instance=p), 'error': 2})
                    elif Place.objects.filter(address = address, user=request.user.get_username()).count() > 0:
                        return render(request, "addMyPlace.html", {'form': PlaceForm(instance=p), 'error': 2})
                    else:
                        latitude = addressData['results'][0]['geometry']['location']['lat']
                        longitude = addressData['results'][0]['geometry']['location']['lng']
                        print(latitude)
                        print(longitude)
                        p.user = request.user.get_username()
                        p.latitude = latitude
                        p.longitude = longitude
                        p.address = address
                        p.save()
            else:
                print('invalid')
            return redirect("/home/")
        else:
            return redirect("/invalid/")

@csrf_exempt
def delete(request):
    if request.user.is_authenticated:
        id = request.GET['id']
        if request.GET['property'] == 'rental':
            p = Property.objects.get(id=id)
            p.delete()
        else:
            p = Place.objects.get(id=id)
            p.delete()
        return redirect("/home/")
    else:
        return redirect("/invalid/")

@csrf_exempt
def update(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            request.session['id'] = request.GET['id']
            if request.GET['property'] == 'rental':
                p = Property.objects.get(id=request.GET['id'])
                f = PropertyForm(instance=p)
                f.fields['address'].widget.attrs.update({'readonly': 'readonly','style':'background-color: rgb(200,200,200)'})
                return render(request, "updateRental.html", {'form': f})
            else:
                p = Place.objects.get(id=request.GET['id'])
                f = PlaceForm(instance=p)
                f.fields['address'].widget.attrs.update({'readonly': 'readonly', 'style': 'background-color: rgb(200,200,200)'})
                return render(request, "updatePlace.html", {'form': f})
        if request.method == 'POST':
            if request.GET['property'] == 'rental':
                p = Property.objects.get(id=request.session['id'])
                f = PropertyForm(request.POST, instance=p)
                if f.is_valid:
                    f.save()
            else:
                p = Place.objects.get(id=request.session['id'])
                f = PlaceForm(request.POST, instance=p)
                if f.is_valid:
                    f.save()
            return redirect("/home/")
    else:
        return redirect("/invalid/")

@csrf_exempt
def invalid(request):
    return render(request, "invalid.html")

@csrf_exempt
def signout(request):
    logout(request)
    return redirect('/signin/')