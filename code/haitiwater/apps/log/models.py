from django.db import models
from enum import Enum
from django.contrib.auth.models import User


class ActionType(Enum):
    ADD = "Ajouter"
    DELETE = "Supprimer"
    EDIT = "Modifier"


class TableType(Enum):
    element = "Élément du réseau"
    zone = "Zone du réseau"
    consumer = "Consommateur"
    user = "Utilisateur de l'application"
    report = "Rapport mensuel"
    ticket = "Ticket de problème"
    location = "Point géographique"


class Transaction(models.Model):
    user = models.ForeignKey(User, verbose_name="Utilisateur ayant fait la modification",
                             related_name="MadeBy", null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Log(models.Model):
    table_name = models.CharField("Nom de la table", choices=[(i.name, i.value) for i in TableType], max_length=30)
    column_name = models.CharField("Nom de la colonne", max_length=30)
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
