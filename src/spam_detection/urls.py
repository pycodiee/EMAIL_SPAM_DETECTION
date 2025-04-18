from django.urls import path
from spam_detection import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('predict-spam/', views.predict_spam, name='predict_spam')
]
