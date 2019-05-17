from django.urls import path
from .views import newsletter_signup, newsletter_unsubscribe

app_name = 'newsletters'

urlpatterns = [
    path('signup/', newsletter_signup, name='newsletter_signup'),
    path('unsubscribe/', newsletter_unsubscribe, name='newsletter_unsubscribe'),
]
