from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import random
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

#-------------------------------- RUTA HOME --------------------------------#
def home(request):
    user = request.session.get("user")
    return render(request, "home.html", {"user": user})


def login_view(request):
    return render(request, "login.html")

def register(request):
    user = request.session.get("user")

    if user:
        return redirect("home")
    
    if request.method == "POST":
        restaurant_name = request.POST["restaurant_name"]
        name = request.POST["name"]
        lastname = request.POST["lastname"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        if users_collection.find_one({"email": email}):
            return render(request, "register.html", {"error": "Este correo ya está registrado."})

        if role == "restaurante":
            name = restaurant_name;
            lastname = "";

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



#accesos y restricciones 
#   RESTAURATES
def pedidos_restaurante(request):
    user = request.session.get("user")

    if not user or user["role"] != "restaurante":
        return redirect("home")  # Solo restaurantes pueden ver esto

    return render(request, "pedidos_restaurante.html", {"user": user})

def add_order(request):
    user = request.session.get("user")
    if  not user and user["role"] != "restaurante":
        return redirect("home") # Solo restaurantes pueden ver esto

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        flag = 1
        clave = ""

        while (flag):
            clave = randomclave()
            if orders_collection.find_one({"clave": clave}):
                flag = 1
            else:
                flag = 0
          
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            num_contenedor = request.POST["num_contenedor"]

            new_box = {
                "id_user": user["id"],
                "clave": clave,
                "name": name,
                "description": description,
            }

            boxes_collection.insert_one(new_box)
    return redirect ("boxes")

def randomclave():
    valores = "abcdefghijklmnopqrstuvwxyz0123456789"
    clave = ""
    for i in range (1,8):
        numero = random.randint(0, 35)
        clave.append(valores[numero])
    return clave


#   CLIENTES
def mis_pedidos(request):
    user = request.session.get("user")

    if not user or user["role"] != "cliente":
        return redirect("home")  # Solo clientes pueden ver sus pedidos

    return render(request, "mis_pedidos.html", {"user": user})

#   ADMIN
def admin_dashboard(request):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin

    return render(request, "admin_dashboard.html", {"user": user})

def users_list(request):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    usuarios = users_collection.find()  
    usuarios_info = [{"name": usuario["name"], "lastname": usuario["lastname"], "phone": usuario["phone"], "address": usuario["address"], "email": usuario["email"], "role": usuario["role"]} for usuario in usuarios]
    return render(request, "users_list.html", {"usuarios": usuarios_info, "user": user})

def editar_usuario(request, email):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    if request.method == "POST":
        user = users_collection.find_one({"email": email})

        if not user:
            return redirect("users")

        nuevo_nombre = request.POST["name"]
        nuevo_apellido = request.POST["lastname"]
        nuevo_telefono = request.POST["phone"]
        nueva_direccion = request.POST["address"]
        nuevo_rol = request.POST["role"]

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
        return redirect("users") 
    return redirect("users") 

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

    return redirect("users")

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
        ability = request.POST["ability"]

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
            "ability": ability,
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

def box_update(request, key):
    user = request.session.get("user")

    if not user or user["role"] != "elmarro":
        return redirect("home")  # Redirige si no es admin
    
    if request.method == "POST":
        box = boxes_collection.find_one({"key": key})

        new_state = request.POST["state"]
        new_address = request.POST["address"]
        new_details = request.POST["details"]
        new_ability = request.POST["ability"]

        boxes_collection.update_one(
            {"key": key},
            {"$set": {
                "state": new_state,
                "address": new_address,
                "details": new_details,
                "ability": new_ability,
            }}
        )
        return redirect("boxes_list")
    return redirect("boxes_list") 

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
