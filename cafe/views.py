
import logging
import requests

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import ContactEnquiry

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "cafe/home.html")


def send_brevo_email(to_email, subject, body, reply_to=None):
    api_key = settings.BREVO_API_KEY
    sender_email = settings.BREVO_SENDER_EMAIL

    if not api_key or not sender_email:
        raise ValueError("Brevo API key or sender email is missing.")

    payload = {
        "sender": {
            "name": "Bean & Bloom Cafe",
            "email": sender_email
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "textContent": body
    }

    if reply_to:
        payload["replyTo"] = {"email": reply_to}

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        },
        json=payload,
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def contact(request):
    if request.method != "POST":
        return redirect("home")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    if not all([name, email, subject, message]):
        messages.error(request, "Please fill in all required fields.")
        return redirect(f"{reverse('home')}#contact")

    enquiry = ContactEnquiry.objects.create(
        name=name,
        email=email,
        phone=phone,
        subject=subject,
        message=message
    )

    owner_subject = f"New cafe website enquiry: {subject}"

    owner_body = (
        "New enquiry received on Bean & Bloom Cafe website.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone or 'Not provided'}\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{message}\n\n"
        f"Received: {enquiry.created_at:%d %b %Y, %I:%M %p}"
    )

    customer_subject = "We received your message — Bean & Bloom Cafe"

    customer_body = (
        f"Hi {name},\n\n"
        "Thank you for contacting Bean & Bloom Cafe. "
        "We have received your message. Our team will get back to you soon.\n\n"
        f"Your message:\n{message}\n\n"
        "Warm regards,\nBean & Bloom Cafe"
    )

    email_errors = []

    # Owner notification
    try:
        send_brevo_email(
            settings.CAFE_OWNER_EMAIL,
            owner_subject,
            owner_body,
            reply_to=email
        )
    except Exception:
        logger.exception("Owner notification email failed.")
        email_errors.append("Owner notification failed.")

    # Customer confirmation
    try:
        send_brevo_email(
            email,
            customer_subject,
            customer_body
        )
    except Exception:
        logger.exception("Customer confirmation email failed.")
        email_errors.append("Customer confirmation failed.")

    if email_errors:
        messages.warning(
            request,
            "Your enquiry has been saved, but email delivery could not "
            "be completed. Please try again later."
        )
    else:
        messages.success(
            request,
            "Thank you! Your enquiry has been sent successfully."
        )

    return redirect(f"{reverse('home')}#contact")
