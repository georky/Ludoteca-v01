import http
import http.client
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import pytz
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from responses import POST
from .models import Clientes
import requests
from django.http import JsonResponse
import json
import request2
import jsonify
from django.db.models import Count
from .forms import ClienteForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Token de verificacion para la configuracion
TOKEN_ANDERCODE = "ANDERCODE"


def index(request, mensaje=None):
    # Plantilla de logeo para los usuarios 
    return render(request, 'login.html', {'error': mensaje})
@login_required
def inicio(request):
    # Obtén el total de usuarios en la base de datos
    total_enviados = Clientes.objects.count()
    usuariosListados = Clientes.objects.all()
    # Aquí puedes aplicar cualquier filtro si es necesario
    # Por ejemplo, si tienes un filtro específico, aplícalo aquí:
    filtered_users_pend = Clientes.objects.filter(campo3='PENDIENTE').count()
    filtered_users_envia = Clientes.objects.filter(campo3='ENVIADO').count()
    #filtered_pend = filtered_users
    
    # Si no tienes filtro, puedes igualar `filtered_count` a `total_users`
    #filtered_count = total_users
    
    context = {
        'total_env': total_enviados,          # Total de usuarios en la base de datos
        'filtered_count_env': filtered_users_envia,     # Total de usuarios (esto es redundante)
        'filtered_count_pen': filtered_users_pend,
        'usuarios': usuariosListados  # Total de usuarios después de aplicar filtro (aquí iguala al total si no hay filtro)
    }
    return render(request, "gestionUsuarios.html", context)

def PerfilQR(request):
    return render(request, "perfilQR.html")

def listado_usuarios(request):
    # Obtén el término de búsqueda y la página actual de los parámetros de la solicitud
    search_term = request.GET.get('search', '')
    page_number = int(request.GET.get('page', 1))

    # Filtra los usuarios según el término de búsqueda
    #usuarios = Clientes.objects.filter(nombreC__icontains=search_term)  # Puedes ajustar el filtro según tus necesidades
    usuarios = Clientes.objects.all().order_by('-campo6')
    # Configura la paginación
    paginator = Paginator(usuarios, 5)  # 5 usuarios por página
    page_obj = paginator.get_page(page_number)

    # Convierte los usuarios en un formato JSON
    data = {
        'clientes': list(page_obj.object_list.values('nombreC', 'telefono', 'tiempoH', 'campo6', 'campo3', 'campo5')),
        'num_pages': paginator.num_pages,
        'current_page': page_number
    }

    return JsonResponse(data)
def validarUsuario(request):
    # Función para validar los usuarios al momento de logearse 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user
            usuariosListados = Clientes.objects.all()
            return redirect('inicio')
            #return render(request, "gestionUsuarios.html", {"usuarios": "erfecto."})
        else:
            return render(request, 'login.html', {'error': "Algó salió mal en la autenticación. Verifique su usuario y contraseña."})
    return render(request, 'index')

def signout(request):
    # Función para cerrar sesión
    logout(request)
    return redirect('index')

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

def obtener_clientess(request, telefono):
    cliente = Clientes.objects.get(telefono=telefono)
    data = {
        'telefono': cliente.telefono,
        'nombreC': cliente.nombreC,
        'nombreR': cliente.nombreR,
        'campo3': cliente.campo3,
    }
    return JsonResponse(data)    

@csrf_exempt
@require_POST
def editarUsuario(request):
    
    telefono = request.POST.get('telefono')
    nombreC = request.POST.get('nombreC')
    nombreR = request.POST.get('nombreR')
    campo3 = request.POST.get('campo3')
    cliente = Clientes.objects.get(telefono=telefono)
    cliente.nombreC = nombreC
    cliente.nombreR = nombreR
    cliente.campo3 = campo3
    cliente.save()
    return redirect('inicio')
       

def eliminarUsuarios(request, telefono):
  if request.method == 'GET':
     clientes = Clientes.objects.get(telefono=telefono)
     clientes.delete()
     messages.success(request, 'Niñ@ eliminado!')
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

    data = {
    "messaging_product": "whatsapp",
    "to": '593' + telefono,  # Asegúrate de que 'telefono' sea un string sin espacios
    "type": "template",
    "template": {
        "name": "ludoteca_fin",
        "language": {
            "code": "es_MX"
        },
        "components": [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {
                            "link": "https://i.postimg.cc/DZf9DMgn/ludoteca.png"  # Reemplaza con la URL de tu imagen
                        }
                    }
                ]
            }
        ]
    }
}

  #Convertir el diccionaria a formato JSON
    data=json.dumps(data)

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Bearer EAAOttkFM0QUBO0ggpCuImEjTDEZCED138rJbdUZBkJXcsobMbytbvU8B5PwpUMlVdmlD5d2ZB7SSQxskCCrVDCUVwyYgwA1AnUc4KkDB43WATGRAw6I4ZAqAm989rlFTNZAouLRKxiHpZCXt0QPCjUa5QsSHOgayyMVZCLs5V5BsSa3SMZAzvvZAQnttU1uT8jddu1QZDZD"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:


        connection.request("POST","/v20.0/380727461797238/messages", data, headers)
        response = connection.getresponse()
        

        print(response.status, response.reason)
        
        if response.status == 200:
            print("Mensaje enviado exitosamente")
            messages.success(request, '¡Mensaje Enviado!')
            estado = 'ENVIADO'
            clientes = Clientes.objects.get(telefono=telefono)
            clientes.campo3 = estado
            clientes.save()
        else:
            print("Error al enviar el mensaje")
           # print(response.status_code, response.text)

        
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

def Nuser_list(request):
    total_clients = Clientes.objects.count()  # Obtiene todos los usuarios
    context = {
        'total_clients': total_clients
    }
    #return render(request, "includes/breadcrumb.html.html", context)
    return render(request, "gestionUsuarios.html", {"total_clients": context})