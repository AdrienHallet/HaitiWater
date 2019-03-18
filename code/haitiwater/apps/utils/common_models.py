from ..log.utils import *


def add(name, infos, transaction):
    for field, value in infos.items():
        log_add(name, field, value, transaction)


def delete(name, infos, transaction):
    for field, value in infos.items():
        log_delete(name, field, value, transaction)


def edit(name, infos, old, transaction):
    edited = False
    not_found = False
    id = -1
    for field, value in infos.items():
        if field not in old:
            print(field)
            log_edit(name, field, "Rien", str(value), transaction)
            edited = True
            not_found = True
        elif str(value) != str(old[field]):
            log_edit(name, field, str(old[field]), str(value), transaction)
            edited = True
        if field == "ID":
            id = str(value)
    if edited:
        log_edit(name, "ID", id, id, transaction)
    if not_found:
        for old_field, old_value in old.items():
            if old_field not in infos:
                log_edit(name, old_field, str(old_value), "Rien", transaction)
