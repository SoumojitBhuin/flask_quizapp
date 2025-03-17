# **Quiz Master - V1**

## **Overview**
**Quiz Master - V1** is a multi-user quiz management system designed to help students prepare for exams. The application supports both **admin and user roles**, allowing admins to create and manage quizzes, while users can take quizzes and track their progress.

## **Features**
- **User authentication** (Login/Logout, Session Management)
- **Admin Panel** for managing subjects, chapters, quizzes, and questions
- **Quiz-taking functionality**
- **Score tracking and analytics using Matplotlib**
- **REST API for extending functionalities**

## **Technologies Used**
- **Flask** (Web framework)
- **Flask-SQLAlchemy** (Database ORM)
- **Flask-Login** (User authentication)
- **Flask-WTF** (Form handling)
- **SQLite** (Database)
- **Jinja2** (Templating engine)
- **Bootstrap** (Front-end design)
- **Matplotlib** (Generating statistics and reports)
- **Python-dotenv** (Environment variable management)
- **Flask-RESTful** (API implementation)
- **JavaScript** (Timer implementation)

## **Installation & Setup**
### **Prerequisites**
- Python (>= 3.7)
- pip (Python package manager)

### **Steps to Install**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/quiz-master.git](https://github.com/SoumojitBhuin/flask_quizapp/tree/main
   cd quiz-master
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file and add necessary configurations (e.g., secret key, database URI).

5. Run the application:
   ```bash
   flask run
   ```
6. Open a web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## **Database Schema**
The application follows a relational database structure with tables:
- **User** (Stores user credentials and details)
- **Subject** (Contains subjects available for quizzes)
- **Chapter** (Stores chapters under subjects)
- **Quiz** (Represents quizzes associated with chapters)
- **Question** (Stores quiz questions and multiple-choice answers)
- **Score** (Records quiz scores and timestamps)

## **API Endpoints**
The application exposes **RESTful APIs** for:
- User authentication
- Fetching subjects, chapters, and quizzes
- Retrieving and submitting quiz answers
- Fetching user progress

## **Project Structure**
```
quiz-master/
│── app/
│   ├── static/            # Static files (CSS, images, JS)
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── routes.py          # Flask routes
│   ├── forms.py           # Form handling with Flask-WTF
│   ├── api.py             # API implementation with Flask-RESTful
│── .env                   # Environment variables
│── config.py              # Configuration settings
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
```

## **Contributing**
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.

## **License**
This project is licensed under the MIT License.

## **Contact**
For any queries, reach out to:
- **Author**: Soumojit Bhuin
- **Email**: [soumojitbhuin2004@gmail.com](mailto:soumojitbhuin2004@gmail.com)

---
**Happy Coding! 🚀**
