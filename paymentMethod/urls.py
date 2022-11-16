from django.urls import path
from .views import *


urlpatterns = [
    path('stripe/', CreateCheckOutSession.as_view(), name="stripe"),
    #path('stripe-webhook/', views.stripe_webhook_view, name="stripe"),   
]