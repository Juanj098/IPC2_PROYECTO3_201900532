from django.urls import path
from . import views

urlpatterns =[
    path('sendTweetsyConfi/',views.sendTweetsyConfi,name='sendTweetsyConfi'),
    path('resumenTweets/',views.resumenTweets, name='resumenTweets'),
    path('resumenConfig/', views.resumenConfi, name='resumenConfi') 
]