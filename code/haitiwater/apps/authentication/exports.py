from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.models import ContentType
from ..water_network.models import Element
from ..consumers.models import Consumer

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def connect(request):
    print("Connection !")
    print(request.POST)
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    print(username + " " + password)
    user = authenticate(username=username, password=password)
    if user is not None:
        print("User found")
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return HttpResponse(token.key, status=200)
    else:
        print("User not found")
        return HttpResponse(status=404)


def create(request): #TODO : creation form, create a person
    print("Creation !")
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user = User.objects.create_user(username, '', password)
    user.save()
    print(username+" "+password)
    return HttpResponse(status=200)