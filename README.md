# Bean & Bloom Cafe — Django Demo Website

A responsive cafe website with Home, About, Menu, Contact, location map, and a Django-powered contact form.

## Requirements
- Python 3.10+
- pip

## Setup (Windows)
```bash
cd cafe_website_django
py -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
py manage.py migrate
py manage.py runserver
```
Open http://127.0.0.1:8000/

## Configure email
Edit `.env`:
- `EMAIL_HOST_USER`: your Gmail address
- `EMAIL_HOST_PASSWORD`: a Google App Password (not your normal Gmail password)
- `CAFE_OWNER_EMAIL`: the cafe owner's email address

For Gmail, enable 2-Step Verification and create an App Password in your Google Account. Never upload `.env` to GitHub.

With valid SMTP details, after a customer submits the form:
1. The customer receives an acknowledgement email.
2. The cafe owner receives the customer's name, email, phone, subject and message.
3. The submission is saved in the Django database even if email delivery fails.

Without SMTP configuration, the website still works and contact submissions are saved; emails are printed in the terminal during local development if console backend is selected.

## Admin
Create an admin account:
```bash
py manage.py createsuperuser
```
Visit http://127.0.0.1:8000/admin/ to view contact enquiries.

## Demo details
- Cafe: Bean & Bloom Cafe
- Address: Civil Lines, Prayagraj, Uttar Pradesh, India
- Map: Google Maps search embed for the demo address. Replace it with the real cafe location before using for a client.
- Menu items and prices are sample content. Update them in `cafe/templates/cafe/home.html`.

## Production checklist
- Set `DEBUG=False`
- Use a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Configure HTTPS and a production database
- Configure real SMTP credentials
- Replace demo address, phone, menu, images and map location
