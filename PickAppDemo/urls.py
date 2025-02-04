from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/store", views.register_store, name="register_store"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.get_category, name="get_category"),
    path("create", views.create, name="create"),
    path("view/<int:pid>", views.view_listing, name="view"),
    path("orders", views.orders, name="orders"),
    path("order/<int:pid>", views.view_listing, name="order"),
    path("search", views.search, name="search"),
    path("store/<str:store_name>", views.store, name="store"),
    path("complete/<int:order_id>", views.complete, name="complete")  # pseudo-cancel
]

