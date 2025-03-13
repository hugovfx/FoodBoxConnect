from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.iniciar_sesion, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.cerrar_sesion, name="cerrar_sesion"),
    path("orders/", views.orders, name="orders"),
    path("users/", views.users_list, name="users"),
    path("users/edit/<str:email>/", views.editar_usuario, name="editar_usuario"),
    path("boxes/", views.boxes, name="boxes"),
    path("boxes_list/", views.boxes_list, name="boxes_list"),
    path("boxes_list/edit/<str:key>/", views.box_update, name="box_update"),
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("eliminar_usuario/<str:email>/", views.eliminar_usuario, name="eliminar_usuario"),
    path("api/hello/", views.api_hello, name="api_hello"),  
]
