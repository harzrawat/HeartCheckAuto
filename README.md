
# Heart Stroke Prediction Flask Application

This is a Flask-based web application designed to predict the chances of a heart stroke based on basic medical data. The application uses a logistic regression model trained on medical data to provide predictions. Additionally, it includes features for booking appointments with doctors and managing patient data.

## Features

- **Heart Stroke Prediction**: Users can input their medical data, and the application will predict the likelihood of a heart stroke using a pre-trained logistic regression model.
- **Appointment Booking**: Users can book appointments with doctors, and the data is stored in a PostgreSQL database.
- **OTP Verification**: Secure OTP-based email verification for user authentication.
- **Patient Data Management**: Stores patient data in a PostgreSQL database for future reference.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- PostgreSQL
- Flask
- Flask-Mail
- psycopg2
- pandas
- scikit-learn
- pickle

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/harzrawat/HeartCheckAuto.git
   cd heart-stroke-prediction
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**:
   - Create a database named `dhp`.
   - Update the database connection settings in the `app.py` file if necessary:
     ```python
     conn = psycopg2.connect(
         dbname="your_db_name",
         user="your_username",
         password="your_password",
         host="localhost"
     )
     ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Login and OTP Verification**:
   - Enter your email to receive an OTP.
   - Verify the OTP to proceed.

2. **Heart Stroke Prediction**:
   - Navigate to the prediction page.
   - Enter your medical data and submit the form to get the prediction.

3. **Book an Appointment**:
   - Navigate to the doctor's page.
   - Enter your details and book an appointment.

## File Structure

- `app.py`: Main Flask application file.
- `doc_app.py`: Additional Flask routes for doctor-related functionalities.
- `logistic_regression_model.pkl`: Pre-trained logistic regression model for heart stroke prediction.
- `templates/`: Contains HTML templates for the web pages.
- `static/`: Contains static files like CSS and JavaScript.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.


## Acknowledgments

- Thanks to the developers of Flask, scikit-learn, and other libraries used in this project.
- Special thanks to the open-source community for their contributions.

## Contact

For any questions or feedback, please contact [Harsh Rawat] at [su-23011@sitare.org].
