from django.db import models
from .user.models import User
# Create your models here.

# TABLA TIPO_PRODUCTO
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=50)

    def  __str__(self):
        return self.descripcion
        
class MarcaProducto(models.Model):
    descripcion = models.CharField(max_length=15)

    def  __str__(self):
        return self.descripcion
    
class Mascota(models.Model):
    descripcion = models.CharField(max_length=15)

    def  __str__(self):
        return self.descripcion

# TABLA PRODUCTO

class Boleta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.IntegerField()

    def __str__(self):
        return self.cliente.nombre + " " + self.fecha

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=90)
    precio = models.PositiveIntegerField(default=5990)
    stock = models.PositiveIntegerField(default=0)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    marca = models.ForeignKey(MarcaProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(null=True,blank=True)
    vigente = models.BooleanField(default=False,blank=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    destacado = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.nombre

class CarritoProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.producto.precio * self.cantidad

class CarritoCliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CarritoProducto)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calcular_total(self):
        total = 0
        for aux in self.items.all():
            total += aux.subtotal()
        return total
    