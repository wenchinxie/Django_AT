from django.urls import path,include
from dashboard import views

urlpatterns=[
    path('table-data',views.TableData.as_view()),
    path('macro/Currencies',views.ProductData.as_view())
]