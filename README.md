# OnlineCourseMS 🎓

**OnlineCourseMS** is a backend system for online courses, built with Django + DRF.  
It supports roles **Student**, **Teacher**.

---

## 🚀 Features

### All Users:
- Registration (with role selection: Teacher/Student)
- Authentication via **JWT** (access/refresh tokens)

### Teachers:
- CRUD operations on their own courses
- Add/Remove students to/from their courses
- Add other teachers to a course
- CRUD operations for lectures within their courses
- Add homework assignments
- View homework submissions
- Assign or update grades for submitted homework
- Add comments to grades

### Students:
- View available courses
- View lectures within a course
- View homework assignments
- Submit homework
- View their own submissions and grades
- View and add comments to grades

---

## 📂 Project Structure

```
OnlineCourseMS/
├── config/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── apps/
│   ├── users/             # Users and authentication
│   ├── courses/           # Courses
│   ├── lectures/          # Lectures
│   └── submissions/       # Homework and grades
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Run

1. Clone the project:
   ```bash
   git clone https://github.com/eBelyakovich/OnlineCourseMS.git
   cd OnlineCourseMS
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure PostgreSQL in `config/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'education_db',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Apply migrations and create superuser:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

---

## 📑 API Documentation

Swagger UI available at:
```
http://127.0.0.1:8000/docs/swagger/
```

---

## 🧪 Testing

Run all tests:
```bash
python manage.py test
```

---

## 🔑 Authentication

1. Register:
   ```
   POST /api/users/register/
   ```

2. Obtain JWT token pair:
   ```
   POST /api/token/
   ```

3. Use access token in headers:
   ```
   Authorization: Bearer <your_access_token>
   ```

---

