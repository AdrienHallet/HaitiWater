from .models import Log


def log_add(table, column, value, transaction):
    new_val = Log(action="ADD", table_name=table, column_name=column,
                  new_value=value, transaction=transaction)
    new_val.save()


def log_delete(table, column, value, transaction):
    new_val = Log(action="DELETE", table_name=table, column_name=column,
                  old_value=value, transaction=transaction)
    new_val.save()


def log_edit(table, column, old_val, new_val, transaction):
    new_val = Log(action="EDIT", table_name=table, column_name=column,
                  old_value=old_val, new_value=new_val, transaction=transaction)
    new_val.save()
