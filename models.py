from sqlalchemy.orm import relationship
from main import db
from sqlalchemy import Sequence, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    full_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role=db.Column(db.String(128), nullable=False)


    addresses = relationship('Address', back_populates='user_address')
    phones = relationship('Phone', back_populates='user_phone')
    carts = relationship('Cart', back_populates='user_cart')
    orders = relationship('Order',back_populates='user_order')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Address(db.Model):
    address_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    address = db.Column(db.String(64), index=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))

    user_address = relationship('User',back_populates='addresses')


class Phone(db.Model):
    phone_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    phonenumber = db.Column(db.String(64), index=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))

    user_phone = relationship('User', back_populates='phones')

class Cart(db.Model):
    user_id = db.Column(db.Integer,ForeignKey('user.user_id') , primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    user_cart = relationship('User', back_populates='carts')


class Order(db.Model):
    order_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    Status = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(64), index=True, nullable=False)
    address = db.Column(db.String(64), index=True, nullable=False)


    user_order=relationship('User', back_populates='orders')
    order_products=relationship('OrderProduct', back_populates='order')

    

class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, ForeignKey('order.order_id'),primary_key=True)
    product_id=db.Column(db.Integer,ForeignKey('product.product_id'),primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    product = relationship('Product', back_populates='order_product', uselist=False) 
    
    order = relationship('Order', back_populates='order_products')

class Product(db.Model):
    product_id=db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    product_name=db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(64), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), index=True, nullable=False)

    order_product= relationship('OrderProduct', back_populates='product') 



class Category(db.Model):
    category_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    description = db.Column(db.String(64), index=True, nullable=False)

class ProductCategory(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer, primary_key=True)

"""  
class comment(db.Model):
    comment_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(64), index=True, nullable=False)
    time = db.Column(db.String(64), index=True, nullable=False)

class reply(db.Model):
    comment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(64), index=True, nullable=False)
    time = db.Column(db.String(64), index=True, nullable=False)
"""






