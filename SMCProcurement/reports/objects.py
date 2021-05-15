
class InvItem:
    def __init__(self, item, data):
        self.name = item.name
        self.category = item.category.name
        self.department = item.department.name
        self.supplier = item.supplier.name
        self.item_code = item.item_code
        self.brand = item.brand
        self.model = item.model
        self.description = item.description
        self.unit_price = item.unit_price
        self.qty = item.qty
        self.stock_out = item.stock_out
        self.remarks = [r["remarks"] for r in data if r["id"] == str(item.id)][0]