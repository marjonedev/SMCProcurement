
class InvItem:
    def __init__(self, item, request, data):
        self.name = item.name
        self.category = item.category.name
        self.department = request.department.name
        self.supplier = item.supplier.name
        self.item_code = item.item_code
        self.brand = item.brand
        self.model = item.model
        self.description = item.description
        self.unit_price = item.unit_price
        self.qty = item.qty
        self.stock_out = item.stock_out
        self.remarks = [r["remarks"] for r in data if r["id"] == str(item.id)][0]


class RQItem:
    def __init__(self, item, data):
        self.name = item.item.name
        self.department = item.request.department.name
        self.number = item.request.number
        self.description = item.item.description
        self.user = item.request.user.full_name
        self.date_request = item.request.date_request
        self.date_needed = item.request.date_needed
        self.sy_start = item.request.sy_start
        self.sy_end = item.request.sy_end
        self.qty = item.qty
        self.status = item.status
        self.unit_price = item.item.unit_price
        self.remarks = [r["remarks"] for r in data if r["id"] == str(item.id)][0]