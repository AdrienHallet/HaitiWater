from django.contrib.auth.models import User
from ..utils.common_models import *

def infos(self):
    result = {}
    for field in User._meta.get_fields():
        result[field.name] = self.__getattribute__(field.name)
    return result


def log_add(self, transaction):
    add("User", self.infos(), transaction)


def log_delete(self, transaction):
    delete("User", self.infos(), transaction)


def log_edit(self, old, transaction):
    edit("User", self.infos(), old, transaction)

User.add_to_class("infos",infos)
User.add_to_class("log_add", log_add)
User.add_to_class("log_delete", log_delete)
User.add_to_class("log_edit", log_edit)