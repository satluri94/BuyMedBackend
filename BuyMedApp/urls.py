from django.urls import path
from .views import SignUpView
from .views import LoginView
from .views import ListCartItems, CategoryItems, ViewOrders
from . import views
# from rest_framework.documentation import include_docs_urls
# from rest_framework_swagger.views import get_swagger_view
# from django.urls import re_path

# schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = [
    # path(r'docs/', include_docs_urls(title='BuyMed')),
    path('register/', SignUpView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('cartitem/add/', views.addCartItem, name='cart_items'),
    path('cartitems/', ListCartItems.as_view(), name='get_cartItems'),
    # path('cartitem/remove/', views.removeCartItem, name='cart_items'),
    path('stockitem/add/', views.addStockItem, name='stock_items'),
    path('stockitems/', CategoryItems.as_view(), name='get_stockItems'),
    # path('stockitem/remove/', views.removeCartItem, name='cart_items'),
    path('placeorder/', views.placeOrder, name='place_order'),
    path('vieworder/', ViewOrders.as_view(), name='get_view_orders'),
    # path('docs/', schema_view)
]