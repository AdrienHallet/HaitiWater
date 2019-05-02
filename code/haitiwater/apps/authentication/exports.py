import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from .views import conf_change


@login_required(login_url='/login/')
def edit(request):
    request.user.first_name = request.POST.get("first-name", None)
    request.user.last_name = request.POST.get("last-name", None)
    request.user.email = request.POST.get("email", None)
    request.user.save()
    return conf_change(request)


def connect(request):
    username = request.POST.get("username", None)
    password = request.POST.get("pwd", None)

    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse("Erreur de connexion", status=403)

    token, _ = Token.objects.get_or_create(user=user)
    data = {"token": token.key}

    # filter the Group model for current logged in user instance
    user_group = Group.objects.filter(user=user).first()
    if user_group is None:
        return HttpResponse("Problème à la connexion", status=400)

    data["group"] = user_group.name
    data["zone_name"] = user.profile.zone.name
    data["zone_id"] = user.profile.zone.id
    data["user_name"] = user.first_name + " " + user.last_name
    return HttpResponse(json.dumps(data), status=200)


# No creation form, users will be created from other users in manager datatable
# def create(request):
#     username = request.POST.get("username", None)
#     password = request.POST.get("password", None)
#     user = User.objects.create_user(username, '', password)
#     user.save()
#     return HttpResponse(status=200)
