from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import random
from django.core import signing
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime


#-------------------------------- FUNCIONES --------------------------------#
def randomOrder():
    valores = "0123456789abcABC"
    clave = ""
    for i in range (9):
        numero = random.randint(0, len(valores)-1)
        clave += valores[numero]
    return clave

#-------------------------------- RUTA HOME --------------------------------#
def home(request):
    message = ""
    user = request.session.get("user")
    if request.method == "POST":
        order_key = request.POST.get("order_key")

        order = orders_collection.find_one({"order_key": order_key})

        if order:
            signed_order_key = signing.dumps(order['order_key'])
            return redirect("order", order_key=signed_order_key)
        else:
            message = "Pedido no encontrado."

    return render(request, "home.html", {"user": user,"message":message})

#-------------------------------- RUTA ORDER --------------------------------#
from bson import ObjectId

def order(request, order_key):
    user = request.session.get("user")

    try:
        original_order_key = signing.loads(order_key)
    except signing.BadSignature:
        return redirect("home")

    order = orders_collection.find_one({"order_key": original_order_key})
    if not order:
        return redirect("home")

    box = boxes_collection.find_one({"_id": ObjectId(order['id_box'])})
    if not box:
        return redirect("home")

    boxes = list(boxes_collection.find({"id_owner": ObjectId(box['id_owner'])})) 
    boxNum = len(boxes) 

    boxes_info = [
        {"position": b["position"]} 
        for b in boxes_collection.find({"id_owner": ObjectId(box["id_owner"])}, {"position": 1, "_id": 0})
    ]

    return render(request, "order.html", {
        "user": user,
        "order": order,
        "box": box,
        "boxes": boxes_info, 
        "boxNum": boxNum
    })

def login_view(request):
    return render(request, "login.html")

def register(request):
    user = request.session.get("user")

    if user:
        return redirect("home")

    if request.method == "POST":
        name = request.POST["name"]
        lastname = request.POST["lastname"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = "cliente"

        if users_collection.find_one({"email": email}):
            data = {
                "name": name,
                "lastname": lastname,
                "phone": phone,
                "address": address,
                "email": email,
                "password":password
            }
            return render(request, "register.html", {"error": "Este correo ya está registrado.", "data":data})

        new_user = {
            "name": name,
            "lastname": lastname,
            "phone": phone,
            "address": address,
            "email": email,
            "password": make_password(password),
            "role": role,
        }
        users_collection.insert_one(new_user)
        return redirect("login") 

    return render(request, "register.html")

def restaurant_register(request):
    user = request.session.get("user")

    if user:
        return redirect("home")

    if request.method == "POST":
        name = request.POST["name"]
        cp = request.POST["cp"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = "restaurante"

        if users_collection.find_one({"email": email}):
            data = {
                "name": name,
                "cp": cp,
                "phone": phone,
                "address": address,
                "email": email,
                "password":password
            }
            return render(request, "restaurant_register.html", {"error": "Este correo ya está registrado.", "data":data})

        new_user = {
            "name": name,
            "cp": cp,
            "phone": phone,
            "address": address,
            "email": email,
            "password": make_password(password),
            "role": role,
        }
        users_collection.insert_one(new_user)
        return redirect("login") 

    return render(request, "restaurant_register.html")

#-------------------------------- RUTA INICIAR_SESION --------------------------------#
def iniciar_sesion(request):
    user = request.session.get("user")

    if user:
        return redirect("home")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = users_collection.find_one({"email": email})

        if user and check_password(password, user["password"]):
            request.session["user"] = {
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
            return redirect("home")
        
        return render(request, "login.html", {"error": "Email o contraseña incorrectos."})

    return render(request, "login.html")

def cerrar_sesion(request):
    request.session.flush()
    return redirect("home")

def orders(request):
    user = request.session.get("user")
    return render(request, "orders.html", {"user": user});

#-------------------------------- RUTA PROFILE --------------------------------#
from django.shortcuts import render, redirect
from bson import ObjectId

from django.shortcuts import render, redirect
from bson import ObjectId

from django.shortcuts import render, redirect
from bson import ObjectId

def profile(request):
    user = request.session.get("user")
    if not user:
        return redirect("login")  # Redirige si no hay sesión activa

    user = users_collection.find_one({"email": user["email"]})

    if request.method == "POST":
        new_name = request.POST["name"]
        new_phone = request.POST["phone"]
        new_address = request.POST["address"]

        users_collection.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$set": {"name": new_name, "phone": new_phone, "address": new_address}}
        )
        return redirect("profile")  # Refresca la página después de actualizar

    return render(request, "profile.html", {"user": user})




#accesos y restricciones 
#   RESTAURATES
def restaurant_panel(request):
    user = request.session.get("user")
    if not user or user["role"] != "restaurante":
        return redirect("home")  # Solo restaurantes pueden ver esto
    user = users_collection.find_one({"email":user["email"]})
    return render(request, "restaurant_panel.html", {"user": user})

def restaurant_boxes(request):
    user = request.session.get("user")
    if not user or user["role"] != "restaurante":
        return redirect("home")  # Solo restaurantes pueden ver esto
    
    user = users_collection.find_one({"email": user["email"]})
    boxes = list(boxes_collection.find({"id_owner": ObjectId(user['_id'])}))

    if request.method == "POST":
        serie = request.POST.get("serie")

        if "toggle" in request.POST:
            # Obtener el estado actual
            box = boxes_collection.find_one({"id_owner": ObjectId(user['_id']), "serie": serie})
            new_status = not box.get("on", False)  # Cambia el estado
            boxes_collection.update_one(
                {"id_owner": ObjectId(user['_id']), "serie": serie},
                {"$set": {"on": new_status}}
            )
        else:
            # Actualizar los otros datos de la caja
            name = request.POST["name"]
            position = request.POST["position"]

            boxes_collection.update_one(
                {"id_owner": ObjectId(user['_id']), "serie": serie},
                {"$set": {"name": name, "position": position}}
            )
        
        return redirect("restaurant_boxes")

    return render(request, "restaurant_boxes.html", {"user": user, "boxes": boxes})


def restaurant_addBox(request):
    user = request.session.get("user")
    if not user or user["role"] != "restaurante":
        return redirect("home")  # Solo restaurantes pueden ver esto

    user = users_collection.find_one({"email":user["email"]})

    if request.method == "POST":
        name = request.POST["name"]
        model = request.POST["model"]
        position = request.POST["position"]
        serie = request.POST["serie"]

        if boxes_collection.find_one({"serie": serie}):
            return redirect("restaurant_addBox")

        new_box = {
            "name": name,
            "model": model,
            "state": "inactive",
            "serie": serie,
            "position": position,
            "on": 0,
            "registration_date": datetime.now(),
            "id_owner": ObjectId(user['_id'])
        }
        boxes_collection.insert_one(new_box)
        return redirect("restaurant_addBox") 

    return render(request, "restaurant_addBox.html", {"user": user})

def restaurant_orders(request):
    user = request.session.get("user")
    if not user or user["role"] != "restaurante":
        return redirect("home") # Solo restaurantes pueden ver esto
    
    if request.method == "POST":
        details = request.POST["details"]
        state = request.POST["state"]
        order_key = request.POST["order_key"]
        
        orders_collection.update_one(
            {"order_key": order_key},
            {"$set": {
                "details": details,
                "state": state
            }}
        )

    user = users_collection.find_one({"email":user["email"]})
    orders = list(orders_collection.find({"id_owner":ObjectId(user["_id"])}))

    return render(request, "restaurant_orders.html", {"user": user, "orders":orders})

def generate_order_key():
    values = "1234560AB"
    orden = ""
    for i in range(9):
        numero = random.randint(0, 8);
        orden += values[numero]
    return orden

def add_order(request):
    user = request.session.get("user")
    if not user or user["role"] != "restaurante":
        return redirect("home")  # Solo restaurantes pueden acceder

    # Obtener datos actualizados del usuario
    user = users_collection.find_one({"email": user["email"]})

    # Obtener todas las cajas del restaurante
    cajas = list(boxes_collection.find({"id_owner": user["_id"], "on":True}))
    users = list(users_collection.find({"role": "cliente"}))

    if request.method == "POST":
        serie = request.POST["serie"]  # Se almacena la serie de la caja
        details = request.POST["details"]
        state = request.POST["state"]
        usuario = request.POST["usuario"] 

        if usuario != "none":
            usuario = users_collection.find_one({"email":usuario})

        id_box = boxes_collection.find_one({"serie":serie})

        generar = True;
        while generar:
            order_key = generate_order_key()  # Generar clave única
            if not orders_collection.find_one({"order_key":order_key}):
                generar = False
        
        box_key = generate_order_key()
        

        dateTime = datetime.now()  # Fecha y hora actuales

        new_order = {
            "order_key": order_key,
            "id_box": ObjectId(id_box['_id']),
            "details": details,
            "state": state,
            "dateTime": dateTime,
            "id_owner": ObjectId(user["_id"]),
            "id_customer": ObjectId(usuario["_id"]),
            "box_key":box_key
        }

        orders_collection.insert_one(new_order)
        return redirect ('restaurant_orders')

    return render(request, "new_order.html", {"user": user, "cajas": cajas, "users":users})





def randomclave():
    valores = "abcdefghijklmnopqrstuvwxyz0123456789"
    clave = ""
    for i in range (1,8):
        numero = random.randint(0, 35)
        clave.append(valores[numero])
    return clave


#   CLIENTES
def user_orders(request):
    user = request.session.get("user")

    if not user or user["role"] != "cliente":
        return redirect("home")  # Solo clientes pueden ver sus pedidos

    user = users_collection.find_one({"email": user["email"]})

    orders = list(orders_collection.find({"id_customer": ObjectId(user["_id"])}))

    for order in orders:
        box = boxes_collection.find_one({"_id": order.get("id_box")})  # Buscar la caja
        order["box_position"] = box.get("position", "none") if box else "none"
        order["key"] = box.get("key")

    return render(request, "user_orders.html", {"user": user, "orders": orders})


#ADMIN
def admin_dashboard(request):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    # Conteo de usuarios por tipo
    customers_count = users_collection.count_documents({"role": "cliente"})
    restaurants_count = users_collection.count_documents({"role": "restaurante"})
    admins_count = users_collection.count_documents({"role": "elmarro"})
    
    # Conteo total
    users_count = customers_count + restaurants_count + admins_count
    boxes_count = boxes_collection.count_documents({})
    orders_count = orders_collection.count_documents({})
    
    # Obtener pedidos recientes
    recent_orders = list(orders_collection.find().sort("dateTime", -1).limit(5))
    
    # Enriquecer los datos de pedidos con nombres de restaurantes y clientes
    for order in recent_orders:
        # Obtener nombre del restaurante
        restaurant = users_collection.find_one({"_id": order.get("id_owner")})
        order["restaurant_name"] = restaurant.get("name", "Desconocido") if restaurant else "Desconocido"
        
        # Obtener nombre del cliente
        customer = users_collection.find_one({"_id": order.get("id_customer")})
        order["customer_name"] = customer.get("name", "Desconocido") if customer else "Desconocido"
    
    context = {
        "user": user,
        "customers_count": customers_count,
        "restaurants_count": restaurants_count,
        "admins_count": admins_count,
        "users_count": users_count,
        "boxes_count": boxes_count,
        "orders_count": orders_count,
        "recent_orders": recent_orders
    }
    
    return render(request, "admin_dashboard.html", context)

def admin_users(request):
    user = request.session.get("user")
    
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    users = list(users_collection.find())
    
    return render(request, "admin_users.html", {"user": user, "usuarios": users})

def editar_usuario(request, email):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    if request.method == "POST":
        usuario = users_collection.find_one({"email": email})

        if not usuario:
            return redirect("admin_users")  # Si no encuentra al usuario, redirige

        nuevo_nombre = request.POST["name"]
        nuevo_apellido = request.POST.get("lastname", "")  # Usando .get para manejar campos opcionales
        nuevo_telefono = request.POST["phone"]
        nueva_direccion = request.POST["address"]
        nuevo_rol = request.POST["role"]

        # Actualizar el usuario en la base de datos
        users_collection.update_one(
            {"email": email},
            {"$set": {
                "name": nuevo_nombre,
                "lastname": nuevo_apellido,
                "phone": nuevo_telefono,
                "address": nueva_direccion,
                "role": nuevo_rol
            }}
        )
        
        return redirect("admin_users")  # Redirige a la lista de usuarios después de editar
        
    # Si es una solicitud GET, redirige a la lista de usuarios
    return redirect("admin_users")

def admin_boxes(request):
    user = request.session.get("user")
    
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    # Obtener todas las cajas con sus datos completos
    boxes = list(boxes_collection.find())
    
    # Convertir ObjectId a string para un manejo más sencillo en la plantilla
    for box in boxes:
        if 'id_owner' in box and box['id_owner']:
            # Obtener el nombre del propietario (restaurante) si existe
            owner = users_collection.find_one({"_id": box['id_owner']})
            if owner:
                box['owner_name'] = owner.get('name', 'Sin asignar')
            else:
                box['owner_name'] = 'Sin asignar'
        else:
            box['owner_name'] = 'Sin asignar'
    
    return render(request, "admin_boxes.html", {"user": user, "boxes": boxes})

def admin_orders(request):
    user = request.session.get("user")
    
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    # Obtener todos los restaurantes para el filtro
    restaurants = list(users_collection.find({"role": "restaurante"}))
    
    # Obtener todos los pedidos ordenados por fecha más reciente
    orders = list(orders_collection.find().sort("dateTime", -1))
    
    # Enriquecer los datos de pedidos con información adicional
    for order in orders:
        # Obtener datos del restaurante
        restaurant = users_collection.find_one({"_id": order.get("id_owner")})
        order["restaurant_name"] = restaurant.get("name", "Desconocido") if restaurant else "Desconocido"
        
        # Obtener datos del cliente
        customer = users_collection.find_one({"_id": order.get("id_customer")})
        order["customer_name"] = customer.get("name", "Desconocido") if customer else "Desconocido"
        
        # Obtener datos de la caja
        box = boxes_collection.find_one({"_id": order.get("id_box")})
        order["box_position"] = box.get("position", "Desconocida") if box else "Desconocida"
        
        # Si no hay estado definido, usar "pendiente" como predeterminado
        if "state" not in order or not order["state"]:
            order["state"] = "pendiente"
            
        # Procesar logs de temperatura
        if 'temperature_logs' in order and order['temperature_logs'] and len(order['temperature_logs']) > 0:
            last_temp = order['temperature_logs'][-1]  # Obtiene el último registro
            order['last_temperature_value'] = last_temp.get('value', 'N/A')
            order['last_temperature_timestamp'] = last_temp.get('timestamp', 'N/A')
        else:
            order['last_temperature_value'] = None
            order['last_temperature_timestamp'] = None
            
        # Procesar logs de acceso
        if 'access_logs' in order and order['access_logs'] and len(order['access_logs']) > 0:
            last_access = order['access_logs'][-1]  # Obtiene el último acceso
            order['last_access_timestamp'] = last_access.get('timestamp', 'N/A')
            order['last_access_success'] = last_access.get('success', False)
        else:
            order['last_access_timestamp'] = None
            order['last_access_success'] = None
    
    return render(request, "admin_orders.html", {
        "user": user, 
        "orders": orders,
        "restaurants": restaurants
    })

def admin_update_order(request, order_key):
    user = request.session.get("user")
    
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    if request.method == "POST":
        details = request.POST.get("details")
        state = request.POST.get("state")
        
        # Validar estado
        valid_states = ["pendiente", "en-proceso", "listo", "completado", "cancelado"]
        if state not in valid_states:
            state = "pendiente"  # Estado predeterminado si no es válido
        
        # Ajustar formato si es necesario
        if state == "en-proceso":
            state = "en proceso"
            
        update_data = {
            "details": details,
            "state": state
        }
        
        # Si se marca como completado, registrar la fecha de entrega
        if state == "completado":
            update_data["delivery_date"] = datetime.now()
        
        orders_collection.update_one(
            {"order_key": order_key},
            {"$set": update_data}
        )
        
        return redirect("admin_orders")
    
    return redirect("admin_orders")

#-------------------------------- RUTA ELIMINAR USUARIO --------------------------------#

def eliminar_usuario(request, email):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin

    usuario = users_collection.find_one({"email": email})
    
    if usuario:
        usuario["deleted_by"] = user["email"]
        users_temp_collection.insert_one(usuario)
        
        users_collection.delete_one({"email": email})

    return redirect("admin_users")

#-------------------------------- RUTA BOXES --------------------------------#
def boxes(request):
    user = request.session.get("user")
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin

    if request.method == "POST":
        user = request.session.get("user")
        flag=1
        address = request.POST["address"]
        model = request.POST["model"]
        details = request.POST["details"]

        while(flag):
            key = randomboxkey()
            if boxes_collection.find_one({"key": key}):
                flag=1
            else:
                flag=0

        new_box = {
            "id_owner": "",
            "email_admin": user["email"],
            "key": key,
            "state": "disabled",
            "address": address,
            "model": model,
            "details": details,
        }
        boxes_collection.insert_one(new_box)   
        return redirect("boxes") 
    
    return render(request, "boxes.html", {"user":user})

def randomboxkey():
    valores = "abcdefghijklmnopqrstuvwxyz0123456789"
    key = ""
    for i in range (0,9):
        numero = random.randint(0, 35)
        if((i%3)==0 and i<9 and i>0):
            key += "-"
            key += valores[numero]
        else:
            key += valores[numero]
    return key

#-------------------------------- RUTA BOXES_LIST --------------------------------#
def boxes_list(request):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    boxes = boxes_collection.find()  
    boxes_info = [{
                    "id_owner":box["id_owner"], 
                   "email_admin":box["email_admin"],
                   "key": box["key"],
                   "state": box["state"],
                   "address": box["address"],
                   "model": box["model"],
                   "details": box["details"],
                   "ability": box["ability"],
                   } for box in boxes]
    return render(request, "boxes_list.html", {"boxes": boxes_info, "user": user})

def box_update(request, serie):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    if request.method == "POST":
        box = boxes_collection.find_one({"serie": serie})

        if not box:
            return redirect("admin_boxes")  # Si no encuentra la caja, redirige

        # Obtener los valores del formulario
        new_name = request.POST["name"]
        new_position = request.POST["position"]
        new_state = request.POST["state"]
        new_on = 'on' in request.POST  # Checkbox, estará presente solo si está marcado

        # Actualizar la caja en la base de datos
        update_data = {
            "name": new_name,
            "position": new_position,
            "state": new_state,
            "on": new_on,
            "last_update": datetime.now()
        }
        
        boxes_collection.update_one(
            {"serie": serie},
            {"$set": update_data}
        )
        
        return redirect("admin_boxes")  # Redirige a la lista de cajas después de editar
        
    # Si es una solicitud GET, redirige a la lista de cajas
    return redirect("admin_boxes")

def admin_panel(request):
    user = request.session.get("user")
    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    return render(request, "admin_panel.html", {"user":user})




#---------------------------------------API-----------------------------------------#
from django.http import JsonResponse

def api_hello(request):
    return JsonResponse({'message': 'Hola, Django API funcionando correctamente'})

def api_get_user(request):
    usuarios = users_collection.find()  
    usuarios_info = [{"name": usuario["name"], "lastname": usuario["lastname"]} for usuario in usuarios]
    return JsonResponse(usuarios_info);

def api_search_order(request, orderKey):
    
    order = orders_collection.find_one({"order_key": orderKey}) 
    return render(request, "order.html", {"order":order});



#-------------------------- Pedido ------------------------------#


    

#                       Ejemplo
def plantilla(request):
    return render(request, "plantilla.html");