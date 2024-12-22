from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'core'

urlpatterns = [   #paths for all functions
    path("", views.index, name = 'index'),
    path("login/", views.userlogin, name='login'),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("search/", views.search_view, name="search_view"),
    path("product_detail/<str:name>", views.product_detail_view, name="product_detail"),
    path("category/<str:cat>", views.listcategory, name="category"),
    path("explore/", views.explore, name="explore"),
    path("rent/", views.rent, name="rent"),
    path('password_reset/', views.reset_pass, name='password_reset'),
    path('reset_password/<uidb64>/<token>/', views.reset_pass_done, name='reset_password_done'),
    path("contact/", views.contact, name="contact"),
    path("contact/sent/", views.send_contact, name="cosend_contact"),
    path("rate/", views.rate_product, name = 'rate_product'),
    path("confirm_order/", views.confirm_order, name = 'confirm_order'),
    path("send_confrim_mail/", views.send_confrim_mail, name = 'send_confrim_mail'),
]