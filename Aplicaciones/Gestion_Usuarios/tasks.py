
from celery import shared_task
import http.client
from django.shortcuts import redirect
import request2
import json
import jsonify
from .models import Clientes
from datetime import datetime, timezone
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
   #if not usuarios_listados.exists():
        #print("No hay usuarios pendientes. La tarea se detiene.")
        #return 
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
                    print(f"Mensaje enviado a {telefono}. Estado: {response.status}, Razón: {response.reason}")
                    estado = 'ENVIADO'
                    clientes = Clientes.objects.get(telefono=telefono)
                    clientes.campo3 = estado
                    clientes.save()
                    #return redirect('inicio')
                else:
                    print("Error al enviar el mensaje")
                # print(response.status_code, response.text)     
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
  