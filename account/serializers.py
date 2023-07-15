from rest_framework import serializers
from .models import CuentaCorriente, Transferencia
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    envio = serializers.CharField(
        read_only=True, source='cuenta_origen.user.username')
    recibio = serializers.CharField(
        read_only=True, source='cuenta_destino.user.username')

    class Meta:
        model = Transferencia
        fields = '__all__'


class CuentaSerializer(serializers.ModelSerializer):
    transferencias_enviadas = RegistroSerializer(many=True, read_only=True)
    transferencias_recibidas = RegistroSerializer(many=True, read_only=True)
    nombre = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = CuentaCorriente
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    ahorros = CuentaSerializer(read_only=True, many=True)

    class Meta:
        model = usuario
        fields = ['id', 'ahorros', 'username', 'first_name', 'last_name',
                  'email', 'password']

    def create(self, validated_data):
        user = usuario.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
