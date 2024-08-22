from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("inicio/",views.inicio,name="inicio"),
    path('signout/', views.signout, name='signout'),
    path('validarUsuario/', views.validarUsuario , name="validarUsuario"),
    path('PerfilQR/', views.PerfilQR,name='PerfilQR'),
    path('listado_usuarios/', views.listado_usuarios, name='listado_usuarios'),
    path('registrarUsuarios/', views.registrarUsuarios,name='registrarUsuarios'),
    path('edicionUsuario/<str:telefono>/', views.edicionUsuario,name='edicionUsuario'),
    path('obtener_clientess/<str:telefono>/', views.obtener_clientess, name='obtener_clientess'),
    path('editarUsuario/', views.editarUsuario,name='editarUsuario'),
    path('edit_cliente/<pk>/', views.edit_cliente, name='edit_cliente'),
    path('eliminarUsuarios/<str:telefono>/', views.eliminarUsuarios, name='eliminarUsuarios'),
    path('enviarNotifi/<str:telefono>/<str:nombreC>/<str:mensaje>/', views.enviarNotifi,name='enviarNotifi'),
    ]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


