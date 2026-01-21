from django.urls import path
from .views import product_list, about_page, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),
    path('about/', about_page, name='about_page'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),    
]