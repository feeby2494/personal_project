from api import db

class Expenditure_Item(db.Model):
    __tablename__ = "expenditure_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    total = db.Column(db.Float)
    sales_order_id = db.Column(db.Integer, db.ForeignKey("sales_order.id"), nullable=False)
    happened_on = db.Column(db.DateTime)