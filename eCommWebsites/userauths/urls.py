from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns=[
    path("sign-up/", views.Register_view,name="sign-up")
]