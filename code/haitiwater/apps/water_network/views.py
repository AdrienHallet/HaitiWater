from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('water_network.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'network_element': debug_fill_table(),
    }
    return HttpResponse(template.render(context, request))

def debug_fill_table():
    table = []
    for i in range(1000):
        table.append({
                'id': 1,
                'type': 'Fontaine',
                'address': 'Rue du bois joli, 4',
                'users': 600,
                'state': "En service",
                'volume_m3': 10,
                'volume_gal': 2641.72,
            })
    return table
