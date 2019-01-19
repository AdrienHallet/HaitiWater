from django.http import HttpResponse
from django.template import loader
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('offline.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME
    }
    return HttpResponse(template.render(context, request))