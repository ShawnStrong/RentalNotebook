from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from final.forms import PropertyForm
from final.models import Property
import urllib
import json
import os
import sys

# Zillow API key: X1-ZWz1gebss99q17_4wzn5
# We need to hide the google api key in an OS environment variable since it's sensitive information.
# We access the key using this:
googleApiKey = os.environ.get('GOOGLE_API_KEY')

@csrf_exempt
def signin(request):
    return redirect('home/')

@csrf_exempt
def home(request):
    p = Property.objects.all()
    print(googleApiKey)
    return render(request, "home.html", {'properties': p, 'googleApiKey': googleApiKey})

@csrf_exempt
def getdata(request):
    return redirect('home/')

@csrf_exempt
def add(request):
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
                "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyBeQKOCrIrLMacq-2vXFmbUpUh0GaI-FyM")
            c2 = c1.read()
            addressData = json.loads(c2)
            print(addressData)
            # if this is true then the request was bad
            if addressData['status'] == "ZERO_RESULTS":
                return render(request, "add.html", {'form': PropertyForm(instance=p), 'error': 1})
            else:
                address = addressData['results'][0]['formatted_address']
                # check if this address is already in the database
                if Property.objects.filter(address = address).count() > 0:
                    return render(request, "add.html", {'form': PropertyForm(instance=p), 'error': 2})
                else:
                    latitude = addressData['results'][0]['geometry']['location']['lat']
                    longitude = addressData['results'][0]['geometry']['location']['lng']
                    print(latitude)
                    print(longitude)
                    p.user = "bob"
                    p.latitude = latitude
                    p.longitude = longitude
                    p.address = address
                    p.save()
        return redirect("/home/")
