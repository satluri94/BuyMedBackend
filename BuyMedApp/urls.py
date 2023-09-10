from django.urls import path
from .views import SignUpView
from .views import LoginView
from .views import ListCartItems
from . import views


urlpatterns = [
    path('register/', SignUpView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('cartitem/add/', views.addCartItem, name='cart_items'),
    path('cartitems/', ListCartItems.as_view(), name='get_cartItems')
]