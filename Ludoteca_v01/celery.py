
from __future__ import absolute_import, unicode_literals

from datetime import timedelta
import os
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ludoteca_v01.settings')



app = Celery('Ludoteca_v01')
app.conf.enable_utc = False
app.conf.update(timezone = 'America/Guayaquil')
app.config_from_object(settings, namespace='CELERY')
app.conf.beat_schedule = {
    'task-periodic': {
        'task': 'Aplicaciones.Gestion_Usuarios.tasks.task_periodic',
        'schedule': timedelta(seconds=30),  # Ejecutar cada 30 segundos
    },
   
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')