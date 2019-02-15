from decimal import Decimal
import easygraphics.dialog as dlg


class Sale:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


sales = []
sale = Sale("Cole", Decimal(2.5), 100)
sales.append(sale)

dlg.show_objects(sales)

dlg.show_objects(sales)
