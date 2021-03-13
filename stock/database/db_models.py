import inspect

# TODO: use sqlalchemy ?

class BaseTable:
    def __get_fields__(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))

        return [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]


class InventoryTable(BaseTable):
    __tablename__ = "inventory_table"

    field1 =

    def __init__(self):
        super().__init__(self)
