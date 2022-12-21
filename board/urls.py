from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("mil/create/", views.MilitaryCreateView.as_view(), name="mil_create"),
    path("mil/<int:pk>", views.MilitaryDetailView.as_view(), name="mil_detail"),
    path("mil/<int:pk>/update/", views.MilitaryUpdateView.as_view(), name="mil_update"),
    path("mil/<int:pk>/delete/", views.military_delete, name="mil_delete"),
    path("comment/create/", views.comment_create, name="cmt_create"),
    path("comment/delete/", views.comment_delete, name="cmt_delete"),
    path("comment/update/", views.comment_update, name="cmt_update"),
    path("like/", views.like, name="like"),
    path("image/", views.image, name="image"),
]
