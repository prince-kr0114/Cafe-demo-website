from django.contrib import admin
from .models import ContactEnquiry

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at", "is_replied")
    list_filter = ("is_replied", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_replied",)
