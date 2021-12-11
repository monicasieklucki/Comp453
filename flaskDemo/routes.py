import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Flask, session
from flaskDemo import app, db, bcrypt, cursor
from flaskDemo.forms import RegistrationForm, UpdateCustomerForm, LoginForm, CheckoutForm, UpdateAccountForm #, PostForm, DeptForm,DeptUpdateForm
from flaskDemo.models import User, Customer, CustomerOrder, Item, OrderLine, Payment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    results = Item.query.all()
    return render_template('home.html', results = results)
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    #results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
   #            .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
   #            .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
   # results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
   #           .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
   #return render_template('join.html', title='Join',joined_1_n=results, joined_m_n=results2)
   #return render_template('home.html', title='Home')

@app.route("/about")
def about():

    if not session.get('user') is None:
        print(session['user'])

    #print(session['user'])
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            print(user)
            session["user"] = {  "UserID": user.id, "Username": user.username, "Email": user.email }

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    if not session.get('user') is None:
        print(session['user'])
        session['user'].clear()
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/delete_customer/<CustomerID>/delete", methods=['GET','POST'])
def delete_customer(CustomerID):
    customer = Customer.query.get_or_404(CustomerID)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer information has been deleted!', 'success')
    return redirect(url_for('customer'))

@app.route("/customer", methods=['GET', 'POST'])
@login_required
def customer():
    form = UpdateCustomerForm()
    db.session.flush()
    if form.validate_on_submit():
        print(form.customerId.data)
        customer_update = Customer.query.filter_by(CustomerID=form.customerId.data).first()
        if not customer_update is None:
            print(customer_update)
            setattr(customer_update, 'CustomerFirstName', form.customerFirstName.data)
            setattr(customer_update, 'CustomerLastName', form.customerLastName.data)
            setattr(customer_update, 'CustomerPhone', form.customerPhone.data)
            setattr(customer_update, 'CustomerAddress', form.customerAddress.data)
            setattr(customer_update, 'CustomerCity', form.customerCity.data)
            setattr(customer_update, 'CustomerState', form.customerState.data)
            setattr(customer_update, 'CustomerZipCode', form.customerZipCode.data)   
            db.session.add(customer_update) 
            db.session.commit()
            flash('Customer information has been updated!', 'success')
        return redirect(url_for('customer'))
    elif request.method == 'GET':
        print("get")
        if session.get('user'):
            cursor.execute("SELECT * FROM customer WHERE UserID=" + str(session['user']['UserID']))
            customer = cursor.fetchone()
            print(customer)
            if not customer is None:
                #populate fields
                #print(customer)
                form.customerId.data = customer["CustomerID"]
                form.customerFirstName.data = customer["CustomerFirstName"]
                form.customerLastName.data = customer["CustomerLastName"]
                form.customerPhone.data = customer["CustomerPhone"]
            
                form.customerAddress.data = customer["CustomerAddress"]
                form.customerCity.data = customer["CustomerCity"]
                form.customerState.data = customer["CustomerState"]
                form.customerZipCode.data = customer["CustomerZipCode"]

    return render_template('customer.html', title='Customer Information', form=form)



@app.route("/shoppingcart")
def shoppingcart():
    return render_template('shoppingcart.html', title='Shopping Cart')

#ADD TO CART
#@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
#@login_required
#def update_dept(dnumber):
#    dept = Department.query.get_or_404(dnumber)
 
#    form = DeptForm()
#    if form.validate_on_submit():
#        dname=form.dname.data
#        mgr_ssn=form.mgr_ssn.data
#        mgr_start=form.mgr_start.data
#        db.session.commit()
#        flash('Your department has been updated!', 'success')
#        return redirect(url_for('dept', dnumber=dnumber))
#    elif request.method == 'GET':
#        form.dnumber.data = dept.dnumber
#        form.name.data = dept.dname
#        form.mgr_ssn.data = dept.mgr_ssn
#        form.mgr_start.data = dept.mgr_start
#    return render_template('create_dept.html', title='Update Department',
#                           form=form, legend='Update Department')


@app.route("/delete_item/<ID>/delete")
def delete_item(ID):
    session['cart_item'].pop(int(ID))

    if len(session['cart_item']) == 0:
        session['cart_item'].clear()
    return render_template('shoppingcart.html')

@app.route("/update_qty/<ID>/update/<qty>", methods=['POST'])
def update_qty(ID, qty):
    #session['cart_item'].pop(int(ID))
    print(ID)
    print(qty)
    return render_template('shoppingcart.html')

@app.route("/empty_cart")
def empty_cart():
    session['cart_item'].clear()
    return render_template('shoppingcart.html')


@app.route("/shoppingcart/<ItemID>/add")
def add_item_to_cart(ItemID):
    item = Item.query.get(ItemID)

    print("Add to cart")
    print(item)

    if 'cart_item' in session:
        dict = {"ItemID": int(item.ItemID), "ItemName": item.ItemName, "ItemPrice": float(item.ItemPrice), "ItemImage": item.ItemImage, "Quantity": int(1), "TotalPrice": (int(1) * float(item.ItemPrice))}
        cart = session['cart_item']
        session["cart_item"].append(dict)
    else:
        session['cart_item'] = [{"ItemID": int(item.ItemID), "ItemName": item.ItemName, "ItemPrice": float(item.ItemPrice), "ItemImage": item.ItemImage, "Quantity": int(1), "TotalPrice": (int(1) * float(item.ItemPrice))}]

    return render_template('shoppingcart.html')


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()

    print(form.errors)
    if form.validate_on_submit():
        print("validate form")
        UserID = None
        if not session.get('user') is None:
            UserID = session['user']['UserID']

        customer = Customer(CustomerFirstName=form.customerFirstName.data, CustomerLastName=form.customerLastName.data, CustomerAddress=form.customerAddress.data, CustomerPhone=form.customerPhone.data, CustomerCity=form.customerCity.data, CustomerState=form.customerState.data, CustomerZipCode=form.customerZipCode.data, UserID=UserID)
        db.session.add(customer)
        db.session.commit()
        print(customer.CustomerID)
        order = CustomerOrder(OrderDate=datetime.now(), OrderStatus='Completed', CustomerID= customer.CustomerID, PaymentID=101)
        db.session.add(order)
        db.session.commit()
        print(order.OrderID)
        for item in session['cart_item']:
            orderline = OrderLine(OrderID=order.OrderID, ItemID=item['ItemID'], Quantity=item['Quantity'])
            db.session.add(orderline)
        db.session.commit()
        
        flash('Your order has been placed!', 'success')
        session['cart_item'].clear()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        print(session['user'])
        print(session.get('user'))
        print(type(session.get('user')))
        if session.get('user'):
            cursor.execute("SELECT * FROM customer WHERE UserID=" + str(session['user']['UserID']))
            customer = cursor.fetchone()
            print(customer)
            cursor.execute("SELECT * FROM user WHERE id=" + str(session['user']['UserID']))
            user = cursor.fetchone()
            if not customer is None:
                #populate fields
                print(customer)
                form.customerFirstName.data = customer["CustomerFirstName"]
                form.customerLastName.data = customer["CustomerLastName"]
                form.customerPhone.data = customer["CustomerPhone"]
            
                form.customerAddress.data = customer["CustomerAddress"]
                form.customerCity.data =customer["CustomerCity"]
                form.customerState.data = customer["CustomerState"]
                form.customerZipCode.data = customer["CustomerZipCode"]

            if not user is None:
                form.customerEmail.data = user["email"]

            #else do nothings
            print("no customer info found")

    return render_template('checkout.html', form=form)


#@app.route("/order")
#def order():
    #flask message
    #payment confirmation

#    form = CheckoutForm()
#    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #db.session.add(user)
        #db.session.commit()
#        flash('Your order has been placed!', 'success')
#        return redirect(url_for('home.html'))
#    home()







