from django.urls import path
from . import views

urlpatterns =[
    path('sendTweetsyConfi/',views.sendTweetsyConfi,name='sendTweetsyConfi'),
    path('resumenTweets/',views.resumenTweets, name='resumenTweets'),
    path('resumenConfig/', views.resumenConfi, name='resumenConfi'),
    path('ListHash/<dateMin>_<dateMax>', views.Hashtags,name='Hashtags'),
    path('ListUsers/<dateMin>_<dateMax>', views.Users,name='users'),
    path('ListEmos/<dateMin>_<dateMax>',views.emociones,name='emociones'),
    path('ClearList/', views.ClearList,name='ClearList')
]