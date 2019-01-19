from ..log.utils import *


def add(name, infos, transaction):
    for field, value in infos.items():
        log_add(name, field, value, transaction)


def delete(name, infos, transaction):
    for field, value in infos.items():
        log_delete(name, field, value, transaction)


def edit(name, infos, old, transaction):
    for field, value in infos.items():
        if str(value) != str(old[field]):
            log_edit(name, field, old[field], value, transaction)