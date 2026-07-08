from django.urls import path, include
from . import views

urlpatterns = [
    path("products/", views.products, name="products"),
    
]
