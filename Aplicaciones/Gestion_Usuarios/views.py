import http
import http.client
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import pytz
from datetime import datetime, timedelta
from .models import Clientes
import requests
import json
import request2
import jsonify
from django.db.models import Count
# Token de verificacion para la configuracion
TOKEN_ANDERCODE = "ANDERCODE"


def index(request, mensaje=None):
    # Plantilla de logeo para los usuarios 
    return render(request, 'login.html', {'error': mensaje})

def inicio(request):
    # Plantilla de la primera página al entrar al sistema
    usuariosListados = Clientes.objects.all().order_by('-campo6')
    return render(request, "gestionUsuarios.html", {"usuarios": usuariosListados})


def validarUsuario(request):
    # Función para validar los usuarios al momento de logearse 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user
            usuariosListados = Clientes.objects.all()
            return render(request, "gestionUsuarios.html", {"usuarios": usuariosListados})
            #return render(request, "gestionUsuarios.html", {"usuarios": "erfecto."})
        else:
            return render(request, 'login.html', {'error': "Algó salió mal en la autenticación. Verifique su usuario y contraseña."})
    return render(request, 'login.html')

def signout(request):
    # Función para cerrar sesión
    logout(request)
    return redirect('inicio')

def registrarUsuarios(request):
    if request.method == 'POST':
        telefono = request.POST['txtTelefono']
        nombreC = request.POST['txNombreC']
        nombreR = request.POST['txtNombreR']
        tiempoH = request.POST['numHoras']
        mensaje = request.POST['txmensaje']
        
        local_tz = pytz.timezone('America/Guayaquil')
        fecha_actual = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
        fecha_termina = datetime.now(local_tz) + timedelta(minutes=1)
        fecha_termina_mas_una_hora_str = fecha_termina.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create new client
        Clientes.objects.create(
            telefono=telefono, nombreC=nombreC, nombreR=nombreR,
            tiempoH=tiempoH, mensaje=mensaje, campo3='PENDIENTE',
            campo5=fecha_termina_mas_una_hora_str, campo6=fecha_actual
        )
        messages.success(request, 'Niñ@ registrado!')
        return redirect('inicio')
    return render(request, 'registrarUsuarios.html')  # Render form for GET requests

def edicionUsuario(request, telefono):
    usuario = Clientes.objects.get(telefono=telefono)
    return render(request, "edicionUsuarios.html", {"usuario": usuario})

def editarUsuario(request):
    if request.method == 'POST':
        telefono = request.POST['txtTelefono']
        nombreC = request.POST['txNombreC']
        nombreR = request.POST['txtNombreR']
        tiempoH = request.POST['numHoras']
        
        usuario = Clientes.objects.get(telefono=telefono)
        usuario.nombreC = nombreC
        usuario.nombreR = nombreR
        usuario.tiempoH = tiempoH
        usuario.save()
        
        messages.success(request, '¡Usuario actualizado!')
        return redirect('inicio')
    return render(request, 'edicionUsuarios.html')

def eliminarUsuarios(request, telefono):
  if request.method == 'GET':
     clientes = Clientes.objects.get(telefono=telefono)
     clientes.delete()
     messages.success(request, '¡Usuario eliminado!')
     return redirect('inicio')
  return render(request, 'gestionUsuarios.html')  # Render form for GET requests

    #return redirect('inicio')

def webhook():
    if request2.method == 'GET':
        challenge = verificar_token(request2)
        return challenge
    elif request2.method == 'POST':
        reponse = recibir_mensajes(request2)
        return reponse  # Method Not Allowed

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}),401

def enviarNotifi(request,telefono, nombreC, mensaje):

    data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": '593'+telefono,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": mensaje
            }
    }
  #Convertir el diccionaria a formato JSON
    data=json.dumps(data)

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Bearer EAAOyRshDbC8BOz2bvkJI922HNuXYGgEUtknT4Ajhog5AUAIHg1XzWZCp1ywehhKTPE1mW1upmF8cW0G7Oc8iuza0VPimg7ZCkZBRatCAQakFnscP99o2vH3BPDZCACZAhNIIsblajrlDXszb8jsXilmM25yupCCbZB6rjapXZClvYePtveFPdqI15LTf0ZCFSSU6"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        connection.request("POST","/v19.0/346378921896150/messages", data, headers)
        response = connection.getresponse()
        print(response.status, response.reason)
        messages.success(request, '¡Mensaje Enviado!')
        estado = 'ENVIADO'
        clientes = Clientes.objects.get(telefono=telefono)
        clientes.campo3 = estado
        clientes.save()
        return redirect('inicio')
    except Exception as e:
        print(json.dumps(e))
    finally:
        connection.close()

def recibir_mensajes(request):
    try:
        data = json.loads(request.body)
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']
        return HttpResponse(json.dumps({'message': 'EVENT_RECEIVED'}), content_type='application/json')
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({'message': 'Error en el formato de los datos'}), status=400, content_type='application/json')
