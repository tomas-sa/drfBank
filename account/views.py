
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import viewsets
from .models import CuentaCorriente, Transferencia
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from django.db.models.signals import post_save
from .serializers import CuentaSerializer, UserSerializer, RegistroSerializer
usuario = get_user_model()


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CuentaViewSet(viewsets.ModelViewSet):
    queryset = CuentaCorriente.objects.all()
    serializer_class = CuentaSerializer

    def get_queryset(self):

        user = self.request.user
        return user.ahorros.all()

    def create(self, request):
        user = request.user.id
        moneda = request.data.get('moneda')

        choices = ["USD", "EUR", "ARS"]

        if not user:
            return Response({'error': 'Usuario no encontrado'}, status=400)

        if not moneda:
            return Response({'error': 'Moneda no encontrada'}, status=400)

        if moneda not in choices:
            return Response({'error': 'Moneda no valida'}, status=400)

        cuenta = usuario.objects.get(id=user)

        if not cuenta:
            return Response({'error': 'Cuenta no encontrada'}, status=400)

        cuenta_existente = CuentaCorriente.objects.filter(
            user=cuenta, moneda=moneda).first()

        if cuenta_existente:
            return Response({'error': 'Ya existe una cuenta con la moneda proporcionada'}, status=400)

        cuenta_ahorros = CuentaCorriente.objects.create(
            user=cuenta,
            moneda=moneda,
            dinero=5000
        )

        serializer = CuentaSerializer(cuenta_ahorros)
        return Response(serializer.data, status=201)


# CODIGO QUE CHATGPT PROPORCIONÓ PARA OBTENER ID DE USUARIO LOGGEADO, ABERIGUAR SOBRE ESTO EN GOOGLE

    """ def list(self, request, *args, **kwargs):
        user_id = request.user.id
        print(f"User ID: {user_id}")
        return super().list(request, *args, **kwargs) """


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = usuario.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.data.get('usuario')

        try:
            respuesta = usuario.objects.get(id=user)
        except:
            return Response({'error': 'cuenta no encontrada'}, status=404)
        return Response({'username': respuesta.username}, status=200)


class TransferenciaAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        usuario_origen_id = request.user.id
        usuario_destino_id = request.data.get('usuario_destino_id')
        cantidad = request.data.get('cantidad')
        moneda = request.data.get('moneda')

        cuenta_origen = CuentaCorriente.objects.filter(
            user=usuario_origen_id, moneda=moneda).first()
        cuenta_destino = CuentaCorriente.objects.filter(
            user=usuario_destino_id, moneda=moneda).first()
        print(cuenta_destino)

        if not cuenta_origen:
            return Response({'error': 'Cuenta de origen no encontrada'}, status=400)

        if not moneda:
            return Response({'error': 'debes seleccionar una moneda'}, status=400)

        if not cuenta_destino:
            return Response({'error': 'Cuenta de destino no encontrada'}, status=400)

        if cuenta_origen.dinero < cantidad:
            return Response({'error': 'Saldo insuficiente'}, status=400)

        if cuenta_origen == cuenta_destino:
            return Response({'error': 'No es posible realizar esta transferencia'}, status=400)

        cuenta_origen.dinero -= cantidad
        cuenta_destino.dinero += cantidad

        cuenta_origen.save()
        cuenta_destino.save()

        transferencia = Transferencia.objects.create(
            cuenta_origen=cuenta_origen,
            cuenta_destino=cuenta_destino,
            cantidad=cantidad,
            moneda=moneda
        )

        serializer = RegistroSerializer(transferencia)
        return Response(serializer.data, status=201)

    def get(self, request, *args, **kwargs):
        usuario = request.user.id

        transferencias_origen = Transferencia.objects.filter(
            cuenta_origen__user_id=usuario)
        transferencias_destino = Transferencia.objects.filter(
            cuenta_destino__user_id=usuario)

        transferencias = transferencias_origen | transferencias_destino
        transferencias = transferencias.order_by('-fecha')

        serializer = RegistroSerializer(transferencias, many=True)
        return Response(serializer.data, status=200)


class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            post_save.send(sender=usuario, instance=user,
                           created=True, request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuscarCuenta(APIView):
    def post(self, request):
        id = request.data.get('id')
        moneda = request.data.get('moneda')
        cuentas = CuentaCorriente.objects.filter(user=id, moneda=moneda)
        serializer = CuentaSerializer(cuentas, many=True)
        if not serializer.data:
            return Response({'error': 'cuenta no encontrada'}, status=400)
        return Response(serializer.data)


class Prestamo(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        id = request.user.id
        moneda = request.data.get('moneda')
        cuenta = CuentaCorriente.objects.filter(user=id, moneda=moneda).first()
        print(cuenta.prestamo)
        monto = request.data.get('monto')

        if not cuenta:
            return Response({'error', 'Cuenta no encontrada'})

        if cuenta.prestamo < monto:
            return Response({'error', 'el saldo ingresado excede el monto del prestamo'}, status=405)

        cuenta.prestamo -= monto
        cuenta.dinero += monto
        cuenta.save()
        return Response({'dinero actual: ', cuenta.dinero}, status=200)

    def get(self, request):
        id = request.user.id
        """ moneda = request.data.get('moneda') """
        cuentas = CuentaCorriente.objects.filter(user=id)

        if not cuentas:
            return Response({'error': 'Cuenta no encontrada'})

        serializer = CuentaSerializer(cuentas, many=True)
        return Response(serializer.data, status=200)
