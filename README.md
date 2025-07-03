# Inventory Management System 🛒

A complete **Inventory Management System** built using **Django** and **MySQL** that helps manage products, vendors, farmers, billing, stock, and payments in a structured and user-friendly way.

## 🔧 Features

- ✅ Farmer and Vendor Management
- ✅ Product and Stock Dashboard
- ✅ Bill Generation with PDF-style Invoice View
- ✅ Vendor Purchases and Payments Tracking
- ✅ Reports Section (Stock, Bills, Purchases)
- ✅ Secure User Login and Logout
- ✅ Fully Responsive Bootstrap-based UI

## 🗃️ Folder Structure

inventory_management/
│
├── core/
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── migrations/
│
├── inventory_management/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── home.html
│ ├── farmer_form.html / list.html
│ ├── vendor_form.html / list.html / purchase_form.html / payment_form.html
│ ├── product_form.html / list.html / stock_dashboard.html
│ ├── bill_form.html / list.html / invoice.html
│ └── reports.html
│
├── db.sqlite3
├── manage.py
└── requirements.txt

## 🛠️ Tech Stack

- **Backend**: Django 4.x, Python 3.9+
- **Database**: MySQL
- **Frontend**: HTML, Bootstrap
- **Authentication**: Django built-in auth
- **Invoice Styling**: Custom PDF-style HTML invoice
- **Version Control**: Git & GitHub

## 🔌 Setup Instructions

### ✅ Prerequisites

- Python installed (3.8+)
- MySQL installed and running
- Git
- Virtualenv (optional but recommended)

### 🔄 Installation


# Clone the repo
git clone https://github.com/Arun2004-git/Inventory-Management-System.git
cd Inventory-Management-System

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
⚙️ Database Setup
Create a database in MySQL (e.g. inventory_db)

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Run migrations:

python manage.py makemigrations
python manage.py migrate
Create superuser:

python manage.py createsuperuser
🚀 Run the Server

python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

📷 Screenshots
Home Dashboard

Product List and Stock Indicators

Vendor Purchase Tracking

Invoice Generator View

📌 Future Enhancements
Export reports to Excel or PDF

Email invoice to customer

Real-time notifications

🤝 Author
Made with ❤️ by Arun2004-git

