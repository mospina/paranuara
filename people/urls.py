from django.urls import path
from people import views

urlpatterns = [
    path("", views.PeopleList.as_view()),
    path("<int:index>", views.PersonDetail.as_view()),
]
