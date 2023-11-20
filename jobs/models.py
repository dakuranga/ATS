from django.db import models
from clients.models import Client
from django.utils import timezone 


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FT', 'FT'),
        ('Cont', 'Con'),
        ('C2H', 'C2H'),
        ('Temp', 'Temp'),
        ('Intern', 'Intern'),
    ]
    JOB_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Hold', 'Hold'),
        ('Upcoming', 'Upcoming'),
    ]
    MODE_CHOICES = [
        ('Hybrid', 'Hybrid'),
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
    ]
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    id = models.AutoField(primary_key=True)
    job_code = models.PositiveIntegerField(blank=True, null=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_notes = models.TextField()
    job_location = models.CharField(max_length=100)
    job_mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    job_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='Open')  
    job_work_hours = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    job_attachment = models.FileField(upload_to='job_attachments/', blank=True, null=True)
    job_minimum_experience = models.PositiveIntegerField(blank=True, null=True)
    job_maximum_experience = models.PositiveIntegerField(blank=True, null=True)
    job_harvestor_string = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    job_pay_rate = models.PositiveIntegerField(blank=True, null=True)
    job_bill_rate = models.PositiveIntegerField(blank=True, null=True)
    job_salary_max = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.job_title
