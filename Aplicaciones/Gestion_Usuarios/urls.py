from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="index"),
    path("inicio/",views.inicio,name="inicio"),
    path('validarUsuario/', views.validarUsuario , name="validarUsuario"),
    path('registrarUsuarios/', views.registrarUsuarios,name='registrarUsuarios'),
    path('eliminarUsuarios/<str:telefono>/', views.eliminarUsuarios, name='eliminarUsuarios'),
    path('enviarNotifi/<str:telefono>/<str:nombreC>/<str:mensaje>/', views.enviarNotifi,name='enviarNotifi'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
