from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from db_con import db

users_collection = db["users"]
orders_collection = db["orders"]
boxes_collection = db["boxes"]
users_temp_collection = db["users_temp"]

def registro(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = make_password(request.POST["password"])
        if users_collection.find_one({"username": username}):
            return render(request, "registro.html", {"error": "El usuario ya existe."})
        users_collection.insert_one({"username": username, "email": email, "password": password})
        return redirect("login")
    return render(request, "registro.html")

