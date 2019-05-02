from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from haitiwater.settings import PROJECT_NAME, PROJECT_VERSION


@login_required(login_url='/login/')
def index(request):
    template = loader.get_template('profile.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    return HttpResponse(template.render(context, request))


def conf_change(request):
    template = loader.get_template('infos_changed.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    return HttpResponse(template.render(context, request))
