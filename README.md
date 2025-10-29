# 🎓 Django Learning Hub

A comprehensive e-learning platform built with Django 5.2.7, featuring course management, user authentication, blog system, and role-based access control.

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.0-38bdf8)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [User Roles & Permissions](#-user-roles--permissions)
- [Screenshots](#-screenshots)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 🎯 Core Features

- **📚 Course Management**
  - Browse and view subjects/courses
  - Detailed course pages with tabs (Description, Reviews, Students, Details)
  - Subject categories and filtering
  - Average ratings and review counts
  - Enrolled student tracking

- **👥 User Authentication**
  - Three-tier user system (Superadmin, Admin, User)
  - Secure login/logout
  - Password reset via email
  - Automatic user profile creation
  - Role-based access control

- **📝 Blog System**
  - Public blog viewing with search and category filters
  - Rich blog posts with featured images
  - Comment system for authenticated users
  - Reading time calculation
  - Blog views tracking
  - **Superadmin**: Full CRUD (Create, Read, Update, Delete)
  - **Admin**: Read and Update only
  - Draft and Published status

- **🔐 Security**
  - CSRF protection
  - Password hashing (PBKDF2-SHA256)
  - Token-based password reset
  - Role-based view restrictions
  - Secure session management

- **🎨 Modern UI**
  - Responsive design with Tailwind CSS 4.0
  - Beautiful gradient backgrounds
  - Smooth animations and transitions
  - Mobile-friendly interface
  - Dark mode support (coming soon)

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.7** - High-level Python web framework
- **Python 3.12** - Programming language
- **SQLite** - Database (development)

### Frontend
- **Tailwind CSS 4.0** - Utility-first CSS framework
- **HTML5 & CSS3** - Markup and styling
- **JavaScript** - Client-side interactivity

### Tools & Libraries
- **django-tailwind** - Tailwind CSS integration for Django
- **django-browser-reload** - Auto-reload during development
- **Pillow** - Image processing library
- **python-decouple** - Environment variables management

---

## 📁 Project Structure

```
DjangoProject/
│
├── DjangoProject/              # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── views.py               # Homepage and contact views
│   └── wsgi.py                # WSGI configuration
│
├── MyFirstProject/            # Main application
│   ├── models.py              # Database models
│   │   ├── SampleModel        # Subject/Course model
│   │   ├── SubjectReview      # Review system
│   │   ├── Student            # Student enrollment
│   │   ├── UserProfile        # User type management
│   │   ├── Blog               # Blog posts
│   │   └── BlogComment        # Blog comments
│   │
│   ├── views.py               # View functions
│   │   ├── Authentication     # Login, logout, password reset
│   │   ├── Dashboards         # Admin & user dashboards
│   │   ├── Blog Management    # CRUD operations
│   │   └── Public Views       # Course & blog viewing
│   │
│   ├── forms.py               # Django forms
│   │   ├── LoginForm          # Authentication form
│   │   ├── ForgotPasswordForm # Password reset
│   │   ├── BlogForm           # Blog CRUD
│   │   └── BlogCommentForm    # Comment submission
│   │
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Django admin configuration
│   │
│   └── templates/             # HTML templates
│       └── MyProject/
│           ├── all_html.html          # Course listing
│           ├── subject_detail.html    # Course details
│           ├── login.html             # Login page
│           ├── forgot_password.html   # Password reset
│           ├── reset_password.html    # New password
│           ├── admin_dashboard.html   # Admin panel
│           ├── user_dashboard.html    # User panel
│           ├── blog_list.html         # Public blogs
│           ├── blog_detail.html       # Blog post view
│           ├── blog_manage.html       # Superadmin blog dashboard
│           ├── admin_blog_list.html   # Admin blog dashboard
│           ├── blog_form.html         # Create/Edit blog
│           └── blog_delete.html       # Delete confirmation
│
├── templates/                 # Global templates
│   ├── layout.html           # Base template
│   └── website/
│       └── index.html        # Homepage
│
├── static/                    # Static files
│   └── style.css             # Global styles
│
├── media/                     # User uploaded files
│   └── images/
│
├── theme/                     # Tailwind CSS theme
│   └── static_src/
│       └── src/
│           └── styles.css    # Tailwind source
│
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- Node.js and npm (for Tailwind CSS)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/ayushmittal62/Learning-Hub-Django-Project.git
cd Learning-Hub-Django-Project
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Tailwind CSS Dependencies

```bash
python manage.py tailwind install
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your superadmin account.

### Step 7: Create Test Users (Optional)

Create a file `create_users.py` in the project root:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User
from MyFirstProject.models import UserProfile

# Create Admin User
admin_user = User.objects.create_user(
    username='admin1',
    email='admin1@learninghub.com',
    password='admin123',
    first_name='Admin',
    last_name='User'
)
admin_profile = UserProfile.objects.get(user=admin_user)
admin_profile.user_type = 'admin'
admin_profile.save()
print(f"✅ Created admin user: {admin_user.username}")

# Create Regular User
regular_user = User.objects.create_user(
    username='john',
    email='john@learninghub.com',
    password='user123',
    first_name='John',
    last_name='Doe'
)
print(f"✅ Created regular user: {regular_user.username}")

print("\n✅ All users created successfully!")
```

Run it:

```bash
# Windows PowerShell
Get-Content create_users.py | python manage.py shell

# macOS/Linux
python manage.py shell < create_users.py
```

### Step 8: Run the Development Server

**Terminal 1** - Django Server:
```bash
python manage.py runserver
```

**Terminal 2** - Tailwind CSS (for live CSS compilation):
```bash
python manage.py tailwind start
```

### Step 9: Access the Application

Open your browser and navigate to:
- **Homepage**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Blogs**: http://localhost:8000/blogs/
- **Login**: http://localhost:8000/login/

---

## ⚙️ Configuration

### Email Settings

For password reset functionality, configure email in `settings.py`:

#### Development (Console Backend)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@learninghub.com'
```

#### Production (Gmail SMTP)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use Gmail App Password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Step Verification first
3. Generate app password for "Django App"
4. Copy the 16-character password

### Database Configuration

#### Development (SQLite - Default)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Production (PostgreSQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learninghub_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables (Optional)

Create a `.env` file in project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Update `settings.py`:

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

---

## 📖 Usage

### User Roles & Permissions

#### 🔴 Superadmin
- **Access**: Django admin panel (`/admin/`)
- **Permissions**:
  - Full database access
  - Create, read, update, delete all content
  - User management
  - **Blog**: Full CRUD operations
  - Access to `/blogs/manage/`

#### 🟡 Admin
- **Access**: Custom admin dashboard (`/admin-dashboard/`)
- **Permissions**:
  - View subjects and statistics
  - View all blogs
  - **Blog**: Read and Update only (cannot create or delete)
  - Access to `/blogs/admin-list/`

#### 🟢 User (Regular)
- **Access**: User dashboard (`/user-dashboard/`)
- **Permissions**:
  - Browse and view published content
  - Add comments to blogs
  - View enrolled courses

### Test Accounts

After running `create_users.py`:

| Username | Password  | Role       | Email                    |
|----------|-----------|------------|--------------------------|
| admin1   | admin123  | Admin      | admin1@learninghub.com   |
| john     | user123   | User       | john@learninghub.com     |

**Superadmin**: Create via `python manage.py createsuperuser`

### Common Tasks

#### Create a Blog Post (Superadmin)

1. Login as superadmin
2. Navigate to `/blogs/manage/`
3. Click "Create New Blog"
4. Fill in:
   - Title
   - Category
   - Content
   - Excerpt (optional)
   - Featured Image URL (optional)
   - Status (Draft/Published)
5. Click "Create Blog"

#### Edit a Blog Post (Admin or Superadmin)

1. Login as admin or superadmin
2. Navigate to `/blogs/admin-list/` (admin) or `/blogs/manage/` (superadmin)
3. Click "Edit" button on desired blog
4. Update fields
5. Click "Update Blog"

#### Add a Comment (Any authenticated user)

1. Login to your account
2. Navigate to any published blog
3. Scroll to comments section
4. Write your comment
5. Click "Post Comment"

#### Reset Password

1. Go to `/login/`
2. Click "Forgot Password?"
3. Enter your registered email
4. Check console (development) or email (production) for reset link
5. Click the link and enter new password
6. Login with new credentials

---

## 🔗 API Endpoints

### Public URLs

| URL                  | Method | Description                    |
|----------------------|--------|--------------------------------|
| `/`                  | GET    | Homepage                       |
| `/about/`            | GET    | About page                     |
| `/contact/`          | GET    | Contact page                   |
| `/blogs/`            | GET    | Blog listing (published only)  |
| `/blogs/<slug>/`     | GET    | Blog detail with comments      |

### Authentication URLs

| URL                             | Method | Description              |
|---------------------------------|--------|--------------------------|
| `/login/`                       | GET/POST | User login             |
| `/logout/`                      | GET    | User logout              |
| `/forgot-password/`             | GET/POST | Request password reset |
| `/reset-password/<token>/`      | GET/POST | Reset password         |
| `/password-reset-complete/`     | GET    | Reset success page       |

### Dashboard URLs (Authenticated)

| URL                 | Method | Access      | Description              |
|---------------------|--------|-------------|--------------------------|
| `/admin-dashboard/` | GET    | Admin       | Admin dashboard          |
| `/user-dashboard/`  | GET    | User        | User dashboard           |

### Blog Management URLs

| URL                           | Method | Access            | Description                |
|-------------------------------|--------|-------------------|----------------------------|
| `/blogs/manage/`              | GET    | Superadmin        | Blog management dashboard  |
| `/blogs/admin-list/`          | GET    | Admin/Superadmin  | Admin blog list            |
| `/blogs/create/`              | GET/POST | Superadmin      | Create new blog            |
| `/blogs/<slug>/edit/`         | GET/POST | Admin/Superadmin | Edit blog                 |
| `/blogs/<slug>/delete/`       | GET/POST | Superadmin      | Delete blog                |

### Course/Subject URLs

| URL                    | Method | Description              |
|------------------------|--------|--------------------------|
| `/subjects/`           | GET    | List all subjects        |
| `/subjects/<id>/`      | GET    | Subject detail page      |

---

## 🎨 Screenshots

### Homepage
Beautiful landing page with hero section, features, and call-to-action buttons.

### Course Listing
Browse all available courses with filters, ratings, and enrolled student counts.

### Course Detail
Detailed course page with tabs for description, reviews, enrolled students, and course details.

### Blog System
- **Public View**: Browse and search published blogs
- **Blog Detail**: Read full posts with comments
- **Superadmin Dashboard**: Full CRUD operations
- **Admin Dashboard**: View and edit blogs

### Authentication
- Clean login page with role-based redirection
- Forgot password flow with email reset

### Dashboards
- **Admin Dashboard**: Statistics, subject management, blog editing
- **User Dashboard**: Course browsing and enrollment

---

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Create Sample Data

Use Django shell to create sample subjects, reviews, and students:

```bash
python manage.py shell
```

```python
from MyFirstProject.models import SampleModel, SubjectReview, Student
from django.contrib.auth.models import User

# Create a subject
subject = SampleModel.objects.create(
    name="Python Programming",
    description="Learn Python from scratch",
    type="programming",
    date_time="2024-01-01"
)

# Create a student
student = Student.objects.create(
    name="Alice Johnson",
    location="New York"
)
subject.students.add(student)

# Create a review
user = User.objects.get(username='john')
review = SubjectReview.objects.create(
    subject=subject,
    user=user,
    rating=5,
    comment="Excellent course!"
)
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ayush Mittal**

- GitHub: [@ayushmittal62](https://github.com/ayushmittal62)
- Email: ayushmittal629@gmail.com
- Repository: [Learning-Hub-Django-Project](https://github.com/ayushmittal62/Learning-Hub-Django-Project)

---

## 🙏 Acknowledgments

- Django Software Foundation for the amazing framework
- Tailwind CSS team for the utility-first CSS framework
- All contributors and supporters

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/ayushmittal62/Learning-Hub-Django-Project/issues) page
2. Create a new issue with detailed description
3. Contact via email: ayushmittal629@gmail.com

---

## 🗺️ Roadmap

### Upcoming Features

- [ ] User registration system
- [ ] Course enrollment functionality
- [ ] Quiz and assessment system
- [ ] Certificate generation
- [ ] Payment integration
- [ ] Real-time notifications
- [ ] Advanced search with Elasticsearch
- [ ] REST API with Django REST Framework
- [ ] Mobile app (React Native)
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Video upload and streaming
- [ ] Live chat support
- [ ] Analytics dashboard
- [ ] Social media integration

---

## 📊 Project Statistics

- **Models**: 7 (SampleModel, SubjectReview, Student, UserProfile, StudentProfile, Blog, BlogComment)
- **Views**: 15+ (Authentication, Dashboards, Blog CRUD, Public Views)
- **Templates**: 15+ HTML files
- **User Roles**: 3 (Superadmin, Admin, User)
- **Python Files**: 50+ files
- **Lines of Code**: 3000+ LOC

---

## 🔧 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'tailwind'`**
```bash
pip install django-tailwind
python manage.py tailwind install
```

**Issue: Tailwind CSS not loading**
```bash
# Make sure both servers are running:
# Terminal 1:
python manage.py runserver

# Terminal 2:
python manage.py tailwind start
```

**Issue: Database errors after migration**
```bash
python manage.py migrate --run-syncdb
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic
```

**Issue: Password reset email not sending**
- Check `EMAIL_BACKEND` in settings.py
- For development, use console backend (check terminal)
- For production, verify SMTP credentials

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Python Documentation](https://docs.python.org/3/)
- [Django Tailwind Package](https://github.com/timonweb/django-tailwind)

---

**⭐ If you find this project helpful, please give it a star!**

---

*Last Updated: October 29, 2025*
