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

    
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='registration/reset_password_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='registration/password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='registration/password_reset_complete'),
]