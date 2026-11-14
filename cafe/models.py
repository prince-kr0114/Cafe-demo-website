from django.db import models

class ContactEnquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact enquiry"
        verbose_name_plural = "Contact enquiries"

    def __str__(self):
        return f"{self.name} — {self.subject}"
