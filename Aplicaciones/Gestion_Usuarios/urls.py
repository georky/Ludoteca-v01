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
    path('registrarUsuarios/', views.registrarUsuarios,name='registrarUsuarios'),
    path('editarUsuario/', views.editarUsuario,name='editarUsuario'),
    path('edicionUsuario/<str:telefono>/', views.edicionUsuario,name='edicionUsuario'),
    path('eliminarUsuarios/<str:telefono>/', views.eliminarUsuarios, name='eliminarUsuarios'),
    path('enviarNotifi/<str:telefono>/<str:nombreC>/<str:mensaje>/', views.enviarNotifi,name='enviarNotifi'),
    ]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


