from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("increase/<int:cart_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:cart_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("orders/", views.orders, name="orders"),
]

