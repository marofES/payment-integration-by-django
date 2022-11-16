from django.shortcuts import redirect
from rest_framework.reverse import reverse
import uuid
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.conf import settings
import os

from django.core.mail import send_mail

from urllib import response
from django.shortcuts import render
from rest_framework import generics, status, views, permissions

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from rest_framework.response import Response

from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings

from django.urls import reverse

from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect, HttpResponse
import os

from pathlib import Path
import stripe
import json

stripe.api_key=settings.STRIPE_SECRET_KEY
API_URL="https://127.0.0.1:8000/"
SITE_URL="https://127.0.0.1:8000/"

# For Recat and Django integrate --> https://www.youtube.com/watch?v=rKD5bhoTeFw&ab_channel=HenryCodingstack

class CreateCheckOutSession(APIView):
    def post(self, request, args, *kwargs):

        #print('STRIPE_SECRET_KEY ',settings.STRIPE_SECRET_KEY)
        #prod_id=self.kwargs["pk"]
        try:

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        
                        'price_data': {
                            'currency':'usd',
                             #'unit_amount':int(product.price) * 100,
                             'unit_amount':1500,
                             'product_data':{

                                'name':'service_name',
                                 #'images':[f"{API_URL}/{product.product_image}"]

                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'product_id':'product.id',
                    'cus_id':'customer_id',
                    'cus_name':'cus_name',
                    'cus_email':'marof145215@gmail.com',
                },
                mode='payment',
                #success_url=settings.SITE_URL + '?success=true',
                success_url=SITE_URL + '?success=true',
                #cancel_url=settings.SITE_URL + '?canceled=true',
                cancel_url=SITE_URL + '?canceled=true',
            )
            print('checkout_session ',checkout_session)
            #return redirect(checkout_session.url)
            return Response({'checkout_session_url':checkout_session.url},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    sig_header = request.headers['STRIPE_SIGNATURE']
    #sig_header = request.headers.get('stripe-signature')
    #print('sig_header ',sig_header)
    event = None
    #print('settings.STRIPE_SECRET_WEBHOOK ',settings.STRIPE_SECRET_WEBHOOK)
    try:
        #print('event ',event)
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SECRET_WEBHOOK)

        #print('event try af ',event)

    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)
    #print('-----------------------------')
    if event['type'] == 'checkout.session.completed':
        #print('event if ',event)
        session = event['data']['object']

        #print('session ',session)
        customer_email=session['customer_details']['email'] #here customer email means provider email


        send_mail(
            subject="Payment Sucessfully by Stripe",
            message=f"Your payment is successfully done. you payment amount {session['amount_total']} USD",
            recipient_list=[session['metadata']['cus_email']],
            from_email=settings.EMAIL_HOST_USER
        )

        #creating payment history
        # user=User.objects.get(email=customer_email) or None

        #PaymentHistory.objects.create(product=product, payment_status=True)
    # Passed signature verification
    return HttpResponse(status=200)