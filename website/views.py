from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .model import User, Profileform
from datetime import datetime
import qrcode,io,base64
from io import BytesIO

from . import db



views=Blueprint('views',__name__)
@views.route('/')
def index():
    return render_template("index.html")

@views.route('/delete_profile/<int:profile_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_profile(profile_id, user_id):
    profile = Profileform.query.get(profile_id)
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.delete(profile)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.signup'))
    

@views.route('/update_profile/<int:profile_id>', methods=['GET','POST'])
@login_required
def update_profile(profile_id):
    profile= Profileform.query.get(profile_id)

    if request.method == 'POST':
        profile.name= name = request.form.get('name')
        profile.age= age= request.form.get('age')
        profile.height= height = request.form.get('height')
        profile.weight= weight = request.form.get('weight')
        profile.startdate =startdate= datetime.strptime(request.form.get('startdate'), '%Y-%m-%d')
        profile.enddate = enddate= datetime.strptime(request.form.get('enddate'), '%Y-%m-%d')
        profile.amount =amount= request.form.get('amount')
        profile.account =account= request.form.get('bank')
        profile.receipt = bytes(request.form.get('receipt'), 'utf-8')

        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f'Name: {name}\nAge: {age}\nHeight: {height}\nWeight: {weight}\nStart date: {startdate}\nEnd date: {enddate}\nAmount: {amount}\nAccount: {account}')
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

            
        qr_bytes = io.BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        qr_data = qr_bytes.read()

        profile.qrcode = qr_data

        db.session.commit()
        return redirect(url_for('views.profile'))
    return render_template("update_profile.html", profile=profile, user=current_user)


@views.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first()
    profile = Profileform.query.filter_by(email=user.email).first()
    
        
    
    # Decode the receipt field in the Profileform object
    qr_code_image = base64.b64encode(profile.qrcode).decode('utf-8')
    
    # Convert the decoded QR code image to a data URL format
    qr_code_data_url = "data:image/png;base64,{}".format(qr_code_image)
    
    # Pass the data URL to the template
    return render_template("profile.html", profile=profile, user=user, qr_code_data_url=qr_code_data_url, profile_id=profile.id, user_id=user.id)



@views.route('/profileform', methods=['GET', 'POST'])
@login_required
def profileform():
    email=session['email']
    form = Profileform.query.filter_by(email=email).first()
    if form:
        return redirect(url_for('views.profile'))
    else:
        if request.method =='POST':
            email=session['email']
            name=request.form.get('name')
            age=request.form.get('age')
            height=request.form.get('height')
            weight=request.form.get('weight')
            startdate_str=request.form.get('startdate')
            startdate= datetime.strptime(startdate_str, '%Y-%m-%d')
            enddate_str = request.form.get('enddate')
            enddate = datetime.strptime(enddate_str, '%Y-%m-%d')
            amount=request.form.get('amount')
            account=request.form.get('bank')
            receipt1=request.form.get('receipt')
            receipt = bytes(receipt1, 'utf-8')

            # Generate QR code from form data
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f'Name: {name}\nAge: {age}\nHeight: {height}\nWeight: {weight}\nStart date: {startdate}\nEnd date: {enddate}\nAmount: {amount}\nAccount: {account}')
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save QR code to database
            qr_bytes = io.BytesIO()
            qr_img.save(qr_bytes, format='PNG')
            qr_bytes.seek(0)
            qr_data = qr_bytes.read()

            newform=Profileform(email= email, name=name, age=age, height=height, weight=weight,startdate=startdate, enddate=enddate, amount=amount, account=account, receipt=receipt, qrcode=qr_data)
            db.session.add(newform)
            db.session.commit()
            return redirect(url_for('views.profile'))
    return render_template("profileform.html", user=current_user)
