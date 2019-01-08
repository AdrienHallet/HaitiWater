from django.http import HttpResponse
from django.template import loader

from haitiwater.settings import PROJECT_NAME, PROJECT_VERSION


def index(request):
    template = loader.get_template('authentication.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('profile.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    return HttpResponse(template.render(context, request))