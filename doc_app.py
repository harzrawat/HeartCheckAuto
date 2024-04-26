from flask import Flask, render_template, request, session
import pandas as pd
import pickle
import psycopg2
import warnings
from flask_mail import Mail, Message
from random import randint
import json

warnings.filterwarnings("ignore")

app = Flask(__name__)

# Configuration for Flask-Mail
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'rawatjiharsh@gmail.com'  # Update with your Gmail email
app.config['MAIL_PASSWORD'] = 'lprj qjyw emym ejmx'  # Update with your Gmail password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Secret key for session management
app.secret_key = 'this is my secret key'

# Function to generate and send OTP via email
def send_otp(email):
    # Generate a random OTP
    otp = randint(100000, 999999) 
    # Store OTP in session for verification later
    session['otp'] = otp
    # Compose the email message
    msg = Message(subject='OTP Verification', sender=('Your Name', app.config["MAIL_USERNAME"]), recipients=[email])
    msg.body = f'Your OTP for verification is: {otp}'
    
    try:
        # Send the email
        mail.send(msg)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

@app.route('/')
def login():
    return render_template('doctor_login.html')

@app.route('/send_otp', methods=["POST"])
def send_otp_route():
    # Get the email from the form
    email = request.form['email']
    
    # Send OTP to the provided email
    if send_otp(email):
        # OTP sent successfully, store the email in session for verification
        session['email'] = email
        return render_template('doctor_login.html', email=email)
    else:
        return render_template('doctor_login.html', messege="Wrong credentials. Try again !")

# Route for verifying OTP
@app.route('/verify_otp', methods=["POST"])
def verify_otp():
    # Get the OTP entered by the user
    user_otp = request.form['otp']
    
    # Get the stored OTP from session
    stored_otp = session.get('otp')
    
    # Check if OTPs match
    if stored_otp and user_otp == str(stored_otp):
        # OTP verification successful
        return render_template('doctor.html')
        # return "OTP verification successful. You are now verified."
    else:
        # OTP verification failed
        return render_template('doctor_login.html', messege="Invalid OTP PLEASE TRY AGAIN !")


@app.route('/doctor', methods=['POST'])
def get_doctor_appointments():
    doctor_name = request.form.get('doctor')
    if not doctor_name:
        return "Doctor name not provided."

    try:
        conn = psycopg2.connect(
            dbname="dhp",
            user="postgres",
            password="harsh",
            host="localhost"
        )
        cursor = conn.cursor()

        # Fetch all data from the doctor specific table
        try:
            cursor.execute(f"SELECT * FROM doctor_{doctor_name.replace(' ', '_')}")
        except Exception as e:
            return render_template("doctor.html",messege_no="No User found for selected doctor, Recheck your name once !")

        rows = cursor.fetchall()

        # Store each row in different dictionaries
        appointment_data = []
        for row in rows:
            appointment = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'mobile': row[3],
                'appointment_date': row[4]
            }
            appointment_data.append(appointment)

        cursor.close()
        conn.close()

        return render_template('doctor.html', appointments=appointment_data)
    except Exception as e:
        print("Error:", e)
        return "Error occurred while fetching appointment data."



if __name__ == "__main__":
    app.run(debug=True)
