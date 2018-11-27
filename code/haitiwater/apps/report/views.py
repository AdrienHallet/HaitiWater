from django.http import HttpResponse
from django.template import loader
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('report.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'current_period': 'Septembre',  # Todo Backend
        'water_outlets': [(1, 'Fontaine Bidule'), (2, 'Kiosque Machin'), (3, 'Prise Truc')]
        # Todo Backend. Liste de fontaines sous forme de [ID, Nom] (vu qu'on a pas de champ "nom", on peut utiliser la concaténation type + emplacement)
        # Notez que l'ID est ce que je vais renvoyer via l'API pour le rapport mensuel, donc envoyez l'ID de l'élément, pas simplement l'ID local
    }
    return HttpResponse(template.render(context, request))
