from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.iniciar_sesion, name="login"),
    path("register/", views.register, name="register"),
    path("restaurant_register/", views.restaurant_register, name="restaurant_register"),
    path("logout/", views.cerrar_sesion, name="cerrar_sesion"),
    path("profile/", views.profile, name="profile"),
    path("orders/", views.orders, name="orders"),
    #path("users/", views.users_list, name="users"),
    path("editar_usuario/<str:email>/", views.editar_usuario, name="editar_usuario"),
    path("boxes/", views.boxes, name="boxes"),
    path("boxes_list/", views.boxes_list, name="boxes_list"),
    path("boxes_list/edit/<str:serie>/", views.box_update, name="box_update"),
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("eliminar_usuario/<str:email>/", views.eliminar_usuario, name="eliminar_usuario"),
    path("api/hello/", views.api_hello, name="api_hello"),  
    path("plantilla", views.plantilla, name="plantilla"),
    path("order/<str:order_key>/", views.order, name="order"),
    # Usuarios
    path("ordenes/usuario", views.user_orders, name="user_orders"),

    # Admin
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin_users/", views.admin_users, name="admin_users"),
    path("admin_boxes/", views.admin_boxes, name="admin_boxes"),
    path("admin_orders/", views.admin_orders, name="admin_orders"),
    path("admin/update_order/<str:order_key>/", views.admin_update_order, name="admin_update_order"),

    # Restaurantes
    path("administrar-restaurante/", views.restaurant_panel, name="restaurant_panel"),
    path("administrar-restaurante/registrar-pedido", views.add_order, name="add_order"),
    path("administrar-restaurante/pedidos", views.restaurant_orders, name="restaurant_orders"),
    path("administrar-restaurante/boxes", views.restaurant_boxes, name="restaurant_boxes"),
    path("administrar-restaurante/addBox", views.restaurant_addBox, name="restaurant_addBox"),
]
