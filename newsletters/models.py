from django.db import models

# Create your models here.
class NewsLetterUser(models.Model):
    name = models.CharField(max_length=255)
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Borrador', 'Borrador'),
        ('Publicado', 'Publicado')
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    email = models.ManyToManyField(NewsLetterUser)
    status = models.CharField(max_length=10, choices= EMAIL_STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
