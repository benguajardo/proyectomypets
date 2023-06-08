from .models import *
from rest_framework import serializers

class TipoProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializers(serializers.ModelSerializer):
    #AGREGAMOS LAS CLAVES FORÁNEAS
    tipo = TipoProductoSerializers(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class MarcaProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MarcaProducto
        fields = '__all__'

class MascotaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

#SERIALIZER - VIEWSET - URL



