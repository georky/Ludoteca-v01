from urllib import request
from celery import shared_task
import http.client
from django.shortcuts import redirect
import request2
import json
import jsonify
from django.contrib import messages
from .models import Clientes
from datetime import datetime, timezone,timedelta
import pytz
from django.utils import timezone
@shared_task(bind=True)
def test_func0(bind= True):
    for i in range(10):
        print(i)
    return 'Done'

@shared_task()
def mul(a,b):
    return a * b
TOKEN_ANDERCODE = "ANDERCODE"

def webhook():
    if request2.method == 'GET':
        challenge = verificar_token(request2)
        return challenge
    elif request2.method == 'POST':
        reponse = recibir_mensajes(request2)
        return reponse

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}),401
@shared_task(bind=True)
def task_periodic(request,bind=True):
   fecha_actual = timezone.now()
    # Filtra los usuarios con campo3 igual a 'PENDIENTE' y obtén los valores de campo5
   usuarios_listados  = Clientes.objects.filter(campo3='PENDIENTE')
   if not usuarios_listados.exists():
        print("No hay usuarios pendientes. La tarea se detiene.")
        return 
    # Itera sobre las fechas obtenidas
    
   for usuario in usuarios_listados:
        fecha_termina = usuario.campo5
        telefono = usuario.telefono
        mensaje = usuario.mensaje
        if isinstance(fecha_termina, str):
            fecha_termina = datetime.strptime(fecha_termina, '%Y-%m-%d %H:%M:%S')
          
        if timezone.is_naive(fecha_termina):
            fecha_termina = timezone.make_aware(fecha_termina)
            

        if fecha_termina <= fecha_actual:
            # Preparar el payload para enviar el mensaje a WhatsApp
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": '593'+telefono,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": mensaje
                }
            }

            # Convertir el diccionario a formato JSON
            data_json = json.dumps(data)

            # Configurar los headers para la solicitud HTTP
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer EAAOyRshDbC8BOz2bvkJI922HNuXYGgEUtknT4Ajhog5AUAIHg1XzWZCp1ywehhKTPE1mW1upmF8cW0G7Oc8iuza0VPimg7ZCkZBRatCAQakFnscP99o2vH3BPDZCACZAhNIIsblajrlDXszb8jsXilmM25yupCCbZB6rjapXZClvYePtveFPdqI15LTf0ZCFSSU6"
            }

            # Realizar la conexión HTTPS con la API de WhatsApp de Facebook
            try:
                connection = http.client.HTTPSConnection("graph.facebook.com")
                connection.request("POST", "/v19.0/346378921896150/messages", data_json, headers)
                
                response = connection.getresponse()
                print(f"Mensaje enviado a {telefono}. Estado: {response.status}, Razón: {response.reason}")
                estado = 'COMPLETADO'
                usuario.campo3 = estado
                usuario.save()
                # Aquí puedes manejar la respuesta si es necesario
                # Por ejemplo, verificar response.status para asegurarte de que el mensaje se haya enviado correctamente.
                
            except Exception as e:
                print(f"Error al enviar mensaje a {telefono}: {str(e)}")
                
            finally:
                connection.close()
            
def recibir_mensajes(req):
    try:
        req = request2.get_json()
        entry =req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']

      #return jsonify({'message':'EVENT_RECEIVED'})
    except Exception as e:
      return jsonify({'message':'EVENT_RECEIVED'})
  