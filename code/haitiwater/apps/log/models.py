from django.db import models
from enum import Enum
from django.contrib.auth.models import User


class ActionType(Enum):
    ADD = "Ajouter"
    DELETE = "Supprimer"
    EDIT = "Modifier"


class ChoiceType(Enum):
    ACCEPT = "Validé"
    CANCEL = "Refusé"


class TableType(Enum):
    element = "Élément du réseau"
    zone = "Zone du réseau"
    consumer = "Consommateur"
    user = "Utilisateur de l'application"
    report = "Rapport mensuel"
    ticket = "Ticket de problème"
    location = "Point géographique"
    profile = "Profil utilisateur"
    payment = "Payement de consommateur"


class Transaction(models.Model):
    user = models.ForeignKey(User, verbose_name="Utilisateur ayant fait la modification",
                             related_name="MadeBy", null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField("Archivé", default=False)
    date_archived = models.DateField("Date d'archive", null=True)
    action = models.CharField("Choix du supérieur", choices=[(i.name, i.value) for i in ChoiceType], max_length=30,
                              null=True)

    def get_action(self):
        return ChoiceType[self.action].value

    def is_visible(self):
        for user in [user for user in User.objects.all() if user.profile.zone is not None
                                                            and user != self.user and user.username != "admin"]:
            if self.user in user.profile.get_subordinates():
                return True
        return False


class Log(models.Model):
    table_name = models.CharField("Nom de la table", choices=[(i.name, i.value) for i in TableType], max_length=30)
    column_name = models.CharField("Nom de la colonne", max_length=100)
    action = models.CharField("Action", max_length=10, choices=[(i.name, i.value) for i in ActionType])
    # States :
    # Add : old_value is null, new_value is not
    # Delete : old_value is not null, new_value is
    # Edit : new_value and old_value are not null
    old_value = models.CharField("Ancienne valeur", max_length=200, null=True)
    new_value = models.CharField("Nouvelle valeur", max_length=200, null=True)
    transaction = models.ForeignKey(Transaction, verbose_name="Ensemble de modifications",
                                    related_name="transaction", null=False, on_delete=models.CASCADE)

    def get_action(self):
        return ActionType[self.action].value

    def get_table(self):
        return TableType[self.table_name].value
