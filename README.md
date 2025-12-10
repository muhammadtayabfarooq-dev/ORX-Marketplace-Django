# ORX Marketplace (Django)

Lightweight OLX-style classifieds app built with Django 4.2. Focus on backend flows (listings, offers, inquiries, user dashboard) with a minimal dark UI.

## Features
- User auth via Django (login/logout/register) with a simple profile (phone + city).
- Categories seeded via migrations (cars, phones, electronics, home/furniture).
- Listings: create/edit, status (active/reserved/sold), condition, location, price, optional image URL.
- Offers: buyers submit offers on listings, sellers can accept/reject.
- Inquiries: ask seller questions on a listing.
- Dashboard: your listings, offers received/made, profile update.

## Setup
1. Install deps (uses SQLite by default):  
   `pip install -r requirements.txt`
2. Run migrations (includes seeded categories):  
   `python manage.py migrate`
3. Create a superuser (optional, for admin):  
   `python manage.py createsuperuser`
4. Run the dev server:  
   `python manage.py runserver`
5. Browse at `http://127.0.0.1:8000/`

## Notes
- Static assets live in `static/`; templates under `templates/` and `listings/templates/`.
- Update `MEDIA_ROOT`/`STATIC_ROOT` in `orx_marketplace/settings.py` if deploying.
- To tweak look and feel, edit `static/styles.css`.
