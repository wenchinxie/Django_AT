from django.urls import path,include
from automation import views

urlpatterns=[
    path('uploads/',views.upload_file.as_view(),name='uploads/')
]