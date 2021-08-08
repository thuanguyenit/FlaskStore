from itertools import count, product
from operator import mod
import re
from flask import Flask, redirect, url_for, request, render_template, session
from flask.helpers import flash
from flask_wtf import form
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import isnot
from sqlalchemy.util.langhelpers import method_is_overridden
from wtforms.validators import Email
from forms import SignInForm, SignUpForm,AddProductForm,EditProductForm,OrderForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
import fireStore



basedir = os.path.abspath(os.path.dirname('__file__'))
app = Flask(__name__)
app.config['SECRET_KEY'] = '8192hdw8y31993r9128yw98y3yewe13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


#config firebase



def sumOrder(user):
    carts=db.session.query(models.Cart).filter_by(user_id=user.user_id).all()
    sum=0
    for c in carts:
        sum=sum+c.count*db.session.query(models.Product).filter_by(product_id=c.product_id).first().price
    return sum
        

    

@app.route("/",methods=['POST','GET'])
def hello_world():
    userImg = "../static/images/guest.png"
    user_id = session.get('user')    
    user=db.session.query(models.User).filter_by(user_id=user_id).first()
    products = db.session.query(models.Product).all()
    pImgs=[]
    for p in products:
        pImgs.append(fireStore.getProductImg(p.product_id))
    if user_id:
        userImg=fireStore.getUserImg(user_id)        
        return render_template('homepage.html', userImg=userImg, user=user, products=products, pImgs=pImgs)
    
    return render_template('homepage.html', userImg=userImg, user=user, products=products, pImgs=pImgs)
    


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = SignInForm()
    userImg = "../static/images/guest.png"
    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data
        
        user = db.session.query(models.User).filter_by(email=_email).first()
        if user is None:
            flash("❌ Your email does not exist! Check it again or create another account!")
        elif user.check_password(_password):            
            session['user']=user.user_id                    
            return redirect(url_for('user'))
        else:
            flash("Wrong password")


    return render_template('login.html', form=form, userImg=userImg)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    userImg = "../static/images/guest.png"
    if form.validate_on_submit():
        if form.inputPassword.data == form.inputConfirmPassword.data:
            _fullname = form.inputFullName.data
            _email = form.inputEmail.data
            _phone= form.inputPhone.data
            _addr=form.inputAddress.data
            _password = form.inputPassword.data
            if db.session.query(models.User).filter_by(email=_email).count()==0:
                user=models.User(full_name=_fullname,email=_email,role="customer")
                user.set_password(_password)
                db.session.add(user)
                db.session.commit()
                user=db.session.query(models.User).filter_by(email=_email).first()
                db.session.add(models.Phone(user_id=user.user_id,phonenumber=_phone))
                db.session.add(models.Address(user_id=user.user_id,address=_addr))
                db.session.commit()
                fireStore.putDefaultImg(user.user_id)
                session['user']=user.user_id
                return redirect(url_for('user'))
            else:
                flash("❌ Your Email is exist! Please login.")
        else:
            flash("❌ Confirm password is incorrect!")
    return render_template('signup.html', form=form, userImg=userImg)



@app.route("/user", methods=['GET', 'POST'])
def user():
    user_id = session.get('user')    
    user=db.session.query(models.User).filter_by(user_id=user_id).first()
    userImg = fireStore.getUserImg(str(user_id))
    if user is None:     
        return redirect("/")  
    
    else:
        if request.method == 'POST':
            if "accept" in request.form:   
                if request.files['file'].filename != '':                   
                    f = request.files['file']
                    f.save(secure_filename("user"+str(user.user_id)+".png"))  
                    fireStore.putUserImG(user_id)
                    os.remove("user"+str(user.user_id)+".png")
                return redirect(url_for('user'))                
            elif "cancel" in request.form:
                return redirect(url_for('user')) 
            elif "logout" in request.form:
                session['user']=0
                return redirect('/')            

        return render_template("user.html",userImg=userImg, user=user)
      
        

@app.route("/ProductManager", methods=['GET', 'POST'])
def productManager():
    form= AddProductForm()
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))
    if user.role=="manager":
        products=db.session.query(models.Product).all()
        pImgs=[]
        for p in products:
            pImgs.append(fireStore.getProductImg(p.product_id))
        
        if form.submit.data and form.validate():            
            product=models.Product(product_name=form.inputName.data,description=form.inputDes.data, price=form.inputPrice.data, status="Active")
            db.session.add(product)
            db.session.commit()
            p_id=db.session.query(models.Product).count()
            f=request.files['file']
            f.save(secure_filename("product"+str(p_id)+".png")) 
            fireStore.putProductImg(p_id)
            os.remove("product"+str(p_id)+".png")
            return redirect('ProductManager')        
            
        return render_template("productManager.html",userImg=userImg, user=user, products=products, pImgs=pImgs, form=form)
    else:
        return redirect("/")

@app.route("/edit/<int:product_id>", methods=['GET', 'POST'])
def edit(product_id):
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))
    product=db.session.query(models.Product).filter_by(product_id=product_id).first()
    pImg=fireStore.getProductImg(product_id)
    form=EditProductForm()
    if user.role=="manager":        
        
        form.inputStatus.choices=[(1,"Active"),(2,"Inactive")]        
        if form.validate_on_submit():            
            if form.inputStatus.data==1:
                product.product_name=form.inputName.data
                product.description=form.inputDes.data
                product.price=form.inputPrice.data
                product.status='Active'
                flash(form.inputName.data)
                
            else:
                product.product_name=form.inputName.data
                product.description=form.inputDes.data
                product.price=form.inputPrice.data
                product.status='Inactive'           
                
            db.session.commit()     
           
            if request.files['file'].filename != '':
                f=request.files['file']
                f.save(secure_filename("product"+str(product.product_id)+".png")) 
                fireStore.putProductImg(product.product_id)
                os.remove("product"+str(product.product_id)+".png")
            return redirect('/ProductManager') 
        return render_template("editProduct.html",userImg=userImg, user=user, form=form, product=product, pImg=pImg)
    else:
        return redirect("/")

@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    userImg = "../static/images/guest.png"
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    if user:
        userImg = fireStore.getUserImg(str(user.user_id))
    product=db.session.query(models.Product).filter_by(product_id=product_id).first()
    pImg=fireStore.getProductImg(product_id)
    if request.method=='POST':
        if user:
            if "cart" in request.form:
                c=db.session.query(models.Cart).filter_by(user_id=user.user_id, product_id=product_id).first()
                if c:
                    c.count = c.count + 1
                else:
                    c=models.Cart(product_id=product_id, user_id=user.user_id, count=1)
                    db.session.add(c)
                db.session.commit()
        else:
            flash("Please login at first!")
            return redirect('/login')
    return render_template("product.html",userImg=userImg, user=user, product=product, pImg=pImg)

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))

    if user:      
        products = db.session.query(models.Product).all()
        carts = db.session.query(models.Cart).filter_by(user_id=user.user_id).all()
        pImgs=[]
        for p in products:
            pImgs.append(fireStore.getProductImg(p.product_id))

        if request.method=='POST':
            for c in carts:
                if "+"+str(c.product_id) in request.form:
                    c.count=c.count+1
                elif "-"+str(c.product_id) in request.form:
                    if c.count >1:
                        c.count=c.count-1
                elif "r"+str(c.product_id) in request.form:
                    db.session.delete(c)
                    carts.remove(c)
            db.session.commit()

        return render_template("cart.html",products=products, carts=carts, user=user, userImg=userImg, pImgs=pImgs)
    else:
        return redirect('/')

@app.route("/placeOrder", methods=['GET', 'POST'])
def placeOrder():
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))
    if user:      
        products = db.session.query(models.Product).all()
        carts = db.session.query(models.Cart).filter_by(user_id=user.user_id).all()
        pImgs=[]
        
        for p in products:
            pImgs.append(fireStore.getProductImg(p.product_id))
            
        
        if request.method=='POST':
            if len(carts)==0:
                flash("Please add product to your cart")
            if "order" in request.form:               
                order=models.Order(user_id=user.user_id,Status="Delivering",phone=request.form.get('phone'), address=request.form.get('address'))
                db.session.add(order)
                db.session.commit()
                order=db.session.query(models.Order).filter_by(order_id=len(db.session.query(models.Order).all())).first()
                for c in carts:
                    orderProduct=models.OrderProduct(order_id=order.order_id,product_id=c.product_id,count=c.count)
                    db.session.delete(c)
                    db.session.add(orderProduct)
                    db.session.commit()
                    return redirect('/')
                    
                

        return render_template("place.html",products=products, carts=carts, user=user, userImg=userImg, pImgs=pImgs, sum=sumOrder(user),form=form)
    else:
        return redirect('/')

def total(order_id):
    order=db.session.query(models.Order).filter_by(order_id=order_id).first()
    total=0
    for p in order.order_products:
        total=total+p.product.price*p.count
    return total

@app.route("/order", methods=['GET', 'POST'])
def order():
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))
    if user is not None:             
        return render_template("order.html",user=user,userImg=userImg)
    else:
        return redirect("/")

@app.route("/order/detail<int:order_id>", methods=['GET', 'POST'])
def detail(order_id):
    user=db.session.query(models.User).filter_by(user_id=session.get('user')).first()
    userImg = fireStore.getUserImg(str(user.user_id))
    order=db.session.query(models.Order).filter_by(order_id=order_id).first()
    
    if user is not None and order.user_id == user.user_id:
        pImgs=[]
        for p in order.order_products:
            pImgs.append(fireStore.getProductImg(p.product_id))
        return render_template("detail.html",user=user,userImg=userImg, order=order)
    else:
        return redirect("/")




if __name__ == '__main__':  
    app.run(host='127.0.0.1', port='5050', debug=True)
