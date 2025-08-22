# Django Blog Website

This is a Django-powered blog project that showcases a fully functional web application built from scratch using the Django framework.

---

##  Project Overview

This repository contains a web-based blog application featuring:

- Post creation, editing, and deletion
- Dynamic content rendering using Django’s templating system
- Organized project structure with multiple apps (`fewapp`, `myapp`)
- Built-in database support via `db.sqlite3`

---

##  Getting Started

To set up and run the project locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/logesh9342/blog-website.git
cd blog-website

# (Optional) Create a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create an admin user (for site management)
python manage.py createsuperuser

# Run the local development server
python manage.py runserver
