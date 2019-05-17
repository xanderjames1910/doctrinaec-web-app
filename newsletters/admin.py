from django.contrib import admin
from .models import NewsLetterUser, Newsletter

# Register your models here.
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subscription_date',)

admin.site.register(NewsLetterUser, NewsLetterAdmin)
admin.site.register(Newsletter)
