# BrainSpark: Online Course Platform

BrainSpark is a robust, Django-based online course platform that allows instructors to create and sell courses, and students to enroll and learn at their own pace.

## Features

- **Course Management**: Instructors can create, edit, and manage their courses easily.
- **Video Lessons**: High-quality video delivery for course content.
- **User Authentication**: Secure login and registration system with email verification.
- **Course Enrollment**: Students can browse courses and enroll in ones they're interested in.
- **Payment Integration**: Seamless payment processing using Stripe.
- **Progress Tracking**: Students can track their progress through enrolled courses.
- **Responsive Design**: Mobile-friendly interface for learning on any device.

## Technologies Used

- Django 5.0.6
- Python 3.x
- Bootstrap 5
- SQLite (Can be configured for other databases)
- Stripe for payment processing
- django-allauth for authentication
- django-summernote for rich text editing

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/brainspark.git
   cd brainspark
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file:


5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

Visit `http://localhost:8000` to see the application in action.


## Acknowledgments

- Thanks to all the open-source projects that made this possible.
