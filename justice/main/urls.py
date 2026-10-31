from django.urls import path
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('practice-areas/', views.practice_areas, name='practice_areas'),
    path('courts/', views.courts, name='courts'),
    path('advocates/', views.advocates, name='advocates'),
    path('contacts/', views.contacts, name='contacts'),
    path('ai/ask/', views.ai_ask, name='ai_ask'),
]
