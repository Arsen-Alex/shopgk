from django.urls import path
from .views import product_list, about_page, product_detail, register_view, login_view, logout_view

urlpatterns = [
    path('', product_list, name='product_list'),
    path('about/', about_page, name='about_page'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]