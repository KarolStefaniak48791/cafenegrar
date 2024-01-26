from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginPage, name="login"),
    path("o-nas", views.onas, name="o-nas"),
    path("menu", views.menu, name="menu"),
    path("rezerwacja", views.rezerwacja, name="rezerwacja"),
    path("profil", views.profil, name="profil"),
    path('order', views.order_view, name='order_view'),
    path("dziekujemy-zamowienie", views.dziekujemy_zamowienie, name="dziekujemy-zamowienie"),
     path('reserve_table/', views.reserve_table, name='reserve_table'),
    path('dziekujemy-rezerwacja/', views.dziekujemy_rezerwacja, name='dziekujemy-rezerwacja'),
    path('logout/', views.logout_view, name='logout'),
]