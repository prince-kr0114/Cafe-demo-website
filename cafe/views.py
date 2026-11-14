from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import strip_tags
from .models import ContactEnquiry

def home(request):
    return render(request, "cafe/home.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not all([name, email, subject, message]):
            messages.error(request, "Please fill in all required fields.")
            return redirect(f"{reverse('home')}#contact")

        enquiry = ContactEnquiry.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message
        )

        owner_subject = f"New cafe website enquiry: {subject}"
        owner_body = (
            f"New enquiry received on Bean & Bloom Cafe website.\\n\\n"
            f"Name: {name}\\nEmail: {email}\\nPhone: {phone or 'Not provided'}\\n"
            f"Subject: {subject}\\n\\nMessage:\\n{message}\\n\\n"
            f"Received: {enquiry.created_at:%d %b %Y, %I:%M %p}"
        )
        customer_subject = "We received your message — Bean & Bloom Cafe"
        customer_body = (
            f"Hi {name},\\n\\nThank you for contacting Bean & Bloom Cafe. "
            f"We have received your message about '{subject}'. Our team will get back to you soon.\\n\\n"
            f"Your message:\\n{message}\\n\\nWarm regards,\\nBean & Bloom Cafe"
        )

        email_errors = []
        try:
            if settings.CAFE_OWNER_EMAIL:
                send_mail(owner_subject, owner_body, settings.DEFAULT_FROM_EMAIL,
                          [settings.CAFE_OWNER_EMAIL], fail_silently=False)
            else:
                email_errors.append("Owner email is not configured.")
        except Exception as exc:
            email_errors.append(str(exc))

        try:
            send_mail(customer_subject, customer_body, settings.DEFAULT_FROM_EMAIL,
                      [email], fail_silently=False)
        except Exception as exc:
            email_errors.append(str(exc))

        if email_errors:
            messages.warning(
                request,
                "Your enquiry has been saved successfully. Email confirmation could not be sent yet; "
                "the cafe team can still view your message. Please configure SMTP settings."
            )
        else:
            messages.success(request, "Thank you! Your enquiry has been sent. A confirmation email is on its way.")
        return redirect(f"{reverse('home')}#contact")

    return redirect("home")
