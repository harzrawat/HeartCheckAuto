# HeartCheckAuto 🫀🩺

## 📝 Overview

This Flask-based web application is designed to predict heart stroke probabilities using machine learning and provide comprehensive healthcare management features. By leveraging logistic regression and secure authentication, the application offers users insights into their potential heart stroke risks and facilitates doctor appointments.

## ✨ Features

- **Advanced Heart Stroke Prediction**
  - Machine learning-powered risk assessment
  - Comprehensive medical data analysis
  - Precise logistic regression model predictions

- **Secure User Authentication**
  - One-Time Password (OTP) email verification
  - Robust security protocols
  - User data protection

- **Healthcare Management**
  - Doctor appointment booking system
  - Patient data storage and management
  - Seamless PostgreSQL database integration

## 🖥️ Screenshots

### Landing Page
![Landing Page](/static/screenshots/landing_page.png)

### Prediction Interface
![Prediction Interface](/static/screenshots/prediction_interface.png)

### Appointment Booking
![Appointment Booking](/static/screenshots/listed_doctors.png)

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **Machine Learning**: scikit-learn, Logistic Regression
- **Database**: PostgreSQL
- **Authentication**: Flask-Mail, OTP Verification
- **Frontend**: HTML, CSS, JavaScript

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/harzrawat/HeartCheckAuto.git
cd heart-stroke-prediction
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
- Create PostgreSQL database named `dhp`
- Update database credentials in `app.py`

### 5. Run the Application
```bash
python app.py
```

## 🤝 Contributing

We welcome contributions to improve the Heart Stroke Prediction Application!

### Contribution Guidelines

1. **Fork the Repository**
   - Create your personal fork of the project
   - Clone your forked repository

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Changes**
   - Write clear, descriptive commit messages
   - Follow PEP 8 style guidelines
   - Include comments for complex logic

4. **Pull Request Process**
   - Describe your changes in the pull request
   - Include screenshots for visual changes
   - Ensure all tests pass

### Areas for Contribution
- Machine learning model improvements
- UI/UX enhancements
- Additional healthcare features
- Performance optimization
- Bug fixes and documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

### MIT License Highlights
- Commercial use allowed
- Modification permitted
- Distribution allowed
- Private use allowed
- No warranty

## 📞 Contact & Support

**Project Maintainer**: Harsh Rawat
- **Email**: su-23011@sitare.org
- **GitHub**: [harzrawat](https://github.com/harzrawat)

For bugs, feature requests, or support, please [open an issue](https://github.com/harzrawat/HeartCheckAuto/issues).

## 🙏 Acknowledgments

- Flask Community
- scikit-learn Developers
- Open Source Contributors
- Our Dedicated Users

---

**Made with ❤️ by the Heart Stroke Prediction Team**
