from django.db import models
import re

class Client(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    website = models.URLField(max_length=255)  # Increased the max_length
    about_client_attachment = models.FileField(upload_to='Clients/')
    hq = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_clients_count(self):
        return Client.objects.count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.website = standardize_url(self.website)
        super().save(*args, **kwargs)


def standardize_url(url):
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    return url.strip()  
