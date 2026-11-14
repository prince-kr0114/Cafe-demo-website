
import logging
import resend

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import ContactEnquiry

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "cafe/home.html")


def send_resend_email(to_email, subject, body, reply_to=None):
    if not settings.RESEND_API_KEY:
        raise ValueError("Resend API key is not configured.")

    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": "Bean & Bloom Cafe <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "text": body,
    }

    if reply_to:
        params["reply_to"] = reply_to

    return resend.Emails.send(params)


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

    # Send email to cafe owner
    try:
        if settings.CAFE_OWNER_EMAIL:
            send_resend_email(
                settings.CAFE_OWNER_EMAIL,
                owner_subject,
                owner_body,
                reply_to=email
            )
        else:
            email_errors.append("Owner email is not configured.")

    except Exception:
        logger.exception("Owner notification email failed.")
        email_errors.append("Owner notification failed.")

    # Send confirmation email to visitor
    try:
        send_resend_email(
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
            "Your enquiry has been saved successfully, "
            "but email delivery could not be completed."
        )
    else:
        messages.success(
            request,
            "Thank you! Your enquiry has been sent successfully."
        )

    return redirect(f"{reverse('home')}#contact")
