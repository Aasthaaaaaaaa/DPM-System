from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_type_choices = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    user_type = models.CharField(max_length=10, choices=user_type_choices)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)  # Indicates if the user is a doctor
    is_patient = models.BooleanField(default=False) 

    def __str__(self):
        return self.username


from django.conf import settings


CATEGORY_CHOICES = [
    ('Mental Health', 'Mental Health'),
    ('Heart Disease', 'Heart Disease'),
    ('Covid19', 'Covid19'),
    ('Immunization', 'Immunization'),
]

class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')  # Requires `Pillow` library
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    summary = models.TextField(max_length=255)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


