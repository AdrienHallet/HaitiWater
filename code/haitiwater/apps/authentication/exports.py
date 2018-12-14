import json

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from ..authentication.models import Profile
from ..water_network.models import Zone

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def connect(request):
    print("Connection !")
    print(request.POST)
    username = request.POST.get("username", None)
    password = request.POST.get("pwd", None)
    #print(username + " " + password)
    user = authenticate(username=username, password=password)

    if user is not None:
        print("User found")
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        data = {"token": token.key}
        # filter the Group model for current logged in user instance
        query_set = Group.objects.filter(user=user)
        if len(query_set) == 1:
            user_group = query_set[0].name
            data["group"] = user_group
            data["zone_name"] = user.profile.zone.name
            data["zone_id"] = user.profile.zone.id
            data["user_name"] = user.first_name+" "+user.last_name
            return HttpResponse(json.dumps(data), content_type="application/json",
                                status=200)
        else:
            return HttpResponse(status=404)
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