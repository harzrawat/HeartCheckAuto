from flask import Flask, render_template, request, session
import pandas as pd
import pickle
import psycopg2
import warnings
from flask_mail import Mail, Message
from random import randint
import json
import datetime

warnings.filterwarnings("ignore")

app = Flask(__name__)

def create_table(patient_name):
    try:
        conn = psycopg2.connect(
            dbname="dhp",
            user="postgres",
            password="harsh",
            host="localhost"
        )
        cur = conn.cursor()
        
        table_name = "patient_" + patient_name.replace(' ', '_')
        
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                gender VARCHAR(10),
                age INTEGER,
                hypertension BOOLEAN,
                heart_disease BOOLEAN,
                ever_married VARCHAR(5),
                work_type VARCHAR(50),
                Residence_type VARCHAR(50),
                avg_glucose_level FLOAT,
                bmi FLOAT,
                smoking_status VARCHAR(20)
            )
        '''
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)
        return False




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
    return render_template('login.html')

@app.route('/send_otp', methods=["POST"])
def send_otp_route():
    # Get the email from the form
    email = request.form['email']
    
    # Send OTP to the provided email
    if send_otp(email):
        # OTP sent successfully, store the email in session for verification
        session['email'] = email
        return render_template('login.html', email=email)
    else:
        return render_template('login.html', messege="Wrong credentials. Try again !")

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
        return render_template('index.html')
        # return "OTP verification successful. You are now verified."
    else:
        # OTP verification failed
        return render_template('login.html', messege="Invalid OTP PLEASE TRY AGAIN !")


@app.route("/index")
def index1():
    return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route('/form', methods=['POST'])
def heart_predict():
    patient_name = request.form.get('name')
    
    with open("logistic_regression_model.pkl", 'rb') as f:
        model = pickle.load(f)

    if request.method == 'POST':
        input_data = {
            'name': request.form.get('name'),
            'gender':request.form.get('gender'),
            'age': request.form.get('age'),
            'hypertension': request.form.get('hypertension'),
            'heart_disease': request.form.get('heart_disease'),
            'ever_married': request.form.get('ever_married'),
            'work_type': request.form.get('work_type'),
            'Residence_type': request.form.get('Residence_type'),
            'avg_glucose_level': request.form.get('avg_glucose_level'),
            'bmi': request.form.get('bmi'),
            'smoking_status': request.form.get('smoking_status')
        }

        conn = psycopg2.connect(
            dbname="dhp",
            user="postgres",
            password="harsh",
            host="localhost"
        )
        cur = conn.cursor()

        create_table(patient_name)

        table_name = "patient_" + patient_name.replace(' ', '_')


        insert_query = '''
            INSERT INTO {} 
            (name, gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        '''.format(table_name)

        try:
            cur.execute(insert_query, (
                input_data['name'],
                input_data['gender'],
                input_data['age'],
                input_data['hypertension'],
                input_data['heart_disease'],
                input_data['ever_married'],
                input_data['work_type'],
                input_data['Residence_type'],
                input_data['avg_glucose_level'],
                input_data['bmi'],
                input_data['smoking_status']
            ))
            conn.commit()
        except psycopg2.Error as e:
            print("Error inserting data:", e)

        select_query = "SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table_name)
        try:
            cur.execute(select_query)
            lowest_row = cur.fetchone()
        except psycopg2.Error as e:
            print("Error fetching data:", e)
            lowest_row = None

        cur.close()
        conn.close()

        if lowest_row:
            df = pd.DataFrame([lowest_row], columns=[
                'id', 'name', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
                'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'
            ])
            data = df.drop(columns=['id', 'name'])

            chance = round(model.predict_proba(data)[0][1] * 100, 4)
            messege1 = f"You have a {chance}% chance of having a stroke."
            messege2 = f"Prediction: {model.predict(data)}"
            return render_template('prediction.html', messege1=messege1)
        else:
            return "No data found in the table."

def create_doctor_table(doctor_name):
    try:
        conn = psycopg2.connect(
            dbname="dhp",
            user="postgres",
            password="harsh",
            host="localhost"
        )
        cursor = conn.cursor()
        
        # Create doctor specific table if not exists
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS doctor_{doctor_name.replace(' ','_')} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                mobile VARCHAR(15) NOT NULL,
                appointment_date DATE NOT NULL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False

@app.route('/doctor', methods=['POST'])
def book_appointment():
    doctor_name = request.form.get('doctor')
    if not doctor_name:
        return "Doctor name not provided."

    if create_doctor_table(doctor_name):
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        appointment_date = request.form.get('date')

        try:
            conn = psycopg2.connect(
                dbname="dhp",
                user="postgres",
                password="harsh",
                host="localhost"
            )
            cursor = conn.cursor()

            # Insert appointment data into the doctor specific table
            cursor.execute(f"""
                INSERT INTO doctor_{doctor_name.replace(' ', '_')} (name, email, mobile, appointment_date)
                VALUES (%s, %s, %s, %s)
            """, (name, email, mobile, appointment_date))

            conn.commit()
            cursor.close()
            conn.close()
            return render_template("prediction.html", messege_completed="Your appointment has been booked successfully.")
        except Exception as e:
            print("Error:", e)
            return "Error occurred while booking appointment."
    else:
        return "Error occurred while creating tables."





if __name__ == "__main__":
    app.run(debug=True)
