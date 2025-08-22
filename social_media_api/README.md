# Social Media API

## Setup
1. Clone repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Authentication
- **POST** `/auth/register/` → Create user + token
- **POST** `/auth/login/` → Login + token
- **GET/PUT** `/auth/profile/` → Manage profile (requires Token)

## User Model
Custom `User` model extends `AbstractUser` with:
- `bio`
- `profile_picture`
- `followers`
