from django.urls import path
from companies import views

urlpatterns = [
    path('<int:index>', views.CompanyDetail.as_view()),
]
