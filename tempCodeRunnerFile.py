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

            # Fetch all data from the doctor specific table
            cursor.execute(f"SELECT * FROM doctor_{doctor_name.replace(' ', '_')}")
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
            return "Error occurred while booking appointment."
    else:
        return "Error occurred while creating tables."

