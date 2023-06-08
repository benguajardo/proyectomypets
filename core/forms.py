from django import forms
from django.forms import ModelForm
from .models import *

class ProductoForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre:"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio:"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock:"}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese Descripcion:"}))
    destacado = forms.BooleanField()
    class Meta:
        model = Producto
        fields = '__all__'

class TipoProductoForm(ModelForm):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class UsuarioForm(ModelForm):
    usuario = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese usuario:"}))
    contrasena = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese contraseña:"}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese nombre:"}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese apellido:"}))
    correo = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese correo electrónico:"}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese dirección:"}))
    telefono = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese teléfono:"}))
    class Meta:
        model = User
        fields = ['usuario','contrasena','nombre','apellido','correo','direccion','telefono']

class Pago(ModelForm):
    class Meta:
        fields = '__all__'