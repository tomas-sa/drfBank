from django.urls import include, path
from rest_framework import routers
from .views import CuentaViewSet, TransferenciaAPIView, UserCreateAPIView, UserViewSet, UserAPIView, BuscarCuenta, Prestamo

router = routers.DefaultRouter()
router.register(r'ahorros', CuentaViewSet)
router.register(r'usuarios', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('transferencia/', TransferenciaAPIView.as_view(), name='transferencia'),
    path('createuser/', UserCreateAPIView.as_view(), name='createuser'),
    path('getuser/', UserAPIView.as_view(), name='geteuser'),
    path('getcuenta/', BuscarCuenta.as_view(), name='buscarcuenta'),
    path('prestamos/', Prestamo.as_view(), name='prestamo')
]
