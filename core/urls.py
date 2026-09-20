from django.urls import path

from . import views

urlpatterns = [
    path("classificar", views.ClassificarLead.as_view()),
    path("leads", views.LeadList.as_view()),
]
