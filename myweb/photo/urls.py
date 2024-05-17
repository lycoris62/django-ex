from django.urls import path

from . import views

urlpatterns = [
    path(
        "", views.photo_list, name="photo_list"
    ),  # ''는 루트주소, view의 photo_list 함수 호출
    path("photo/<int:pk>", views.photo_detail, name="photo_detail"),
    path("photo/new", views.photo_post, name="photo_post"),
    path("photo/<int:pk>/edit", views.photo_edit, name="photo_edit"),
]
