# ORX Marketplace

A Django-based OLX-style classifieds application focused on solid backend workflows and a clean, dark-themed user interface. Users can create listings, submit offers, and manage inquiries with minimal friction.

---

## Table of Contents

* Features
* Tech Stack
* Project Structure
* Data Model
* Setup
* Running the App
* Admin & Maintenance
* Key User Flows
* Customization Notes
* Author

---

## Features

**Listings:**

* Create and edit listings with title, description, price, category, condition, status (active, reserved, sold), location, optional image URL, and slug-based URLs.

**Categories:**

* Pre-seeded via migration (Cars, Phones, Electronics, Home & Furniture).

**Offers:**

* Authenticated users can submit offers on listings.
* Sellers can accept or reject offers.

**Inquiries:**

* Anyone can submit a question on a listing.
* Logged-in users have their contact details auto-filled.

**Users & Profiles:**

* Django authentication with extended profile fields (phone number, city).
* Dashboard for managing listings, offers made, and offers received.

**Interface:**

* Minimal dark theme with search, filters, pagination, and simple forms.
* Responsive layout using basic CSS.

**Admin:**

* All core models registered for admin management.

---

## Tech Stack

* Python 3.9+
* Django 4.2
* Django Templates and static CSS (no JavaScript build tools required)
* SQLite database by default

---

## Project Structure (Key Files)

```
manage.py
orx_marketplace/        # Settings, URLs, WSGI
listings/               # Models, Views, Forms, URLs, Admin, Signals, Migrations
templates/              # Base layout, listing pages, authentication
static/styles.css       # Styling
requirements.txt
README.md
```

---

## Data Model (Listings App)

**Category**

* name
* slug
* description
* created_at

**Listing**

* title
* slug
* description
* price
* category → Category
* condition
* location
* image_url
* status
* owner → User
* timestamps

**Offer**

* listing → Listing
* offered_by → User
* amount
* message
* status
* created_at

**Inquiry**

* listing → Listing
* sender → User (optional)
* name
* email
* message
* created_at

**UserProfile**

* user → User
* phone_number
* city

Signals automatically create a `UserProfile` when a new user registers.

---

## Setup

Create a virtual environment:

```
python -m venv .venv
```

Activate it (Windows PowerShell):

```
.\venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Apply migrations (includes seeded categories):

```
python manage.py migrate
```

Create a superuser (optional):

```
python manage.py createsuperuser
```

---

## Running the App

Start the development server:

```
python manage.py runserver
```

Open the application:

```
http://127.0.0.1:8000/
```

Authentication routes:

* Login/Logout: `/accounts/`
* Registration: `/register/`

---

## Admin & Maintenance

Admin panel:

```
/admin/
```

Static and media files:

* Configured for local development using `STATIC_URL`, `STATICFILES_DIRS`, `MEDIA_URL`, and `MEDIA_ROOT`.
* Update `STATIC_ROOT` and `MEDIA_ROOT` for production deployments.

Categories may be updated through the admin panel or via new migrations.

---

## Key User Flows

**Browse & Search:**

* Homepage displays active and reserved listings with filters and pagination.

**Listing Detail:**

* View full details, submit inquiries, submit offers, or edit if you are the owner.

**Offers:**

* Buyers submit offers.
* Sellers accept or reject offers.
* Dashboard displays incoming and outgoing offers.

**Dashboard:**

* View all listings owned by the user, offers made, offers received, and update user profile information.

**Authentication:**

* Signup, login, and logout using Django’s built-in authentication system with extended profile fields.

---

## Customization Notes

**Styling:**

* Modify `static/styles.css` to adjust theme colors and layout.

**Profiles:**

* Extend `UserProfile` with additional fields if needed, or switch to a custom user model (before initial migration).

**File Storage:**

* For real image uploads, configure `MEDIA_*` settings or integrate a cloud storage backend.

**Database:**

* Update the `DATABASES` configuration in `settings.py` for MySQL in production.

**Slugs:**

* Automatically generated with collision-safe increment logic in `Listing.save()`.

---

## Author

**Muhammad Tayab Farooq**
Email: **[muhammadtayabfarooq@gmail.com](mailto:muhammadtayabfarooq@gmail.com)**
Experience: **2 years with Python and Django**
