import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Flask, session
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, CheckoutForm, UpdateAccountForm #, PostForm, DeptForm,DeptUpdateForm
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
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
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
        print(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        print(user.password)
        print(form.password.data)
        print(bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        print(bcrypt.check_password_hash(user.password, form.password.data))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
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
        session.clear()
    return render_template('shoppingcart.html')

@app.route("/update_qty/<ID>/update/<qty>", methods=['POST'])
def update_qty(ID, qty):
    #session['cart_item'].pop(int(ID))
    print(ID)
    print(qty)
    return render_template('shoppingcart.html')

@app.route("/empty_cart")
def empty_cart():
    session.clear()
    return render_template('shoppingcart.html')


@app.route("/shoppingcart/<ItemID>/add")
def add_item_to_cart(ItemID):
    item = Item.query.get(ItemID)

    print("Add to cart")

    #print(item.ItemID)
    #print(item.ItemName)
    #print(item.Quantity)

    if 'cart_item' in session:
        dict = {"ItemID": int(item.ItemID), "ItemName": item.ItemName, "ItemPrice": float(item.ItemPrice), "ItemImage": item.ItemImage, "Quantity": int(1), "TotalPrice": (int(1) * float(item.ItemPrice))}
        cart = session['cart_item']
        session["cart_item"].append(dict)
    else:
        session['cart_item'] = [{"ItemID": int(item.ItemID), "ItemName": item.ItemName, "ItemPrice": float(item.ItemPrice), "ItemImage": item.ItemImage, "Quantity": int(1), "TotalPrice": (int(1) * float(item.ItemPrice))}]

    #cart_item = CartItem(product=product)
    #db.session.add(cart_item)
    #db.session.commit()
    #results = Item.query.all()

    return render_template('shoppingcart.html')


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    print(form)
    print("I'm here!")
    print(form.validate_on_submit())

    print(form.errors)
    if form.validate_on_submit():
        print("Validated")
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #db.session.add(user)
        #db.session.commit()
        flash('Your order has been placed!', 'success')
        session['cart_item'].clear()
        return redirect(url_for('home'))
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







