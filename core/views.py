from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework import viewsets
from .serializers import *
import requests


class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializers

class TipoProductoViewset(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializers

# Create your views here.
def descripcion(request):
    return render(request, 'core/descripcion.html')

def suscripcion(request):
    return render(request, 'core/suscripcion.html')

def login(request):
    return render(request, 'core/login.html')

def salir(request):
    logout(request)
    return redirect, ('core/')

def productos(request):
    productosAll = Producto.objects.all()
    usuariosAll = User.objects.all()
    TipoProductoAll = TipoProducto.objects.all()
    data = {
        'listado' : productosAll,
        'listadoUser' : usuariosAll,
        'listadoTipo' : TipoProductoAll
    }
    return render(request,'core/productos.html',data)

def productosapi(request):
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api/dolar')
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    
    productos = respuesta.json()
    monedas = respuesta2.json()
    #ARREGLO PERSONAJES
    envolvente = respuesta3.json()
    personajes = envolvente['results']

    valor_usd = monedas['serie'][0]['valor']

    valor_carrito = 20000
    #TRANSFORMAMOS DE CLP A USD

    valor_final = valor_carrito / valor_usd
    
    data = {

        'productos' : productos,
        'valor' : round(valor_final,2),
        'personajes' : personajes,
    }
    return render(request,'core/productosapi.html',data)
#VIEWS DEL CARRITO



def agregar_al_carrito(request,id):
    producto = Producto.objects.get(id=id)
    carritocli, created = CarritoCliente.objects.get_or_create(usuario=request.user)
    carritoprod, item_created = CarritoProducto.objects.get_or_create(producto=producto, usuario=request.user)
    if not item_created:
        carritoprod.cantidad +=1
        carritoprod.save()
        
    carritocli.items.add(carritoprod)
    carritocli.save()

    return redirect(to='carrito')

def restar_carrito(request, id):
    producto = Producto.objects.get(id=id)
    carritocli, created = CarritoCliente.objects(usuario=request.user)
    carritoprod = carritocli.items.get(producto=producto)
    if carritoprod.cantidad == 0:
        carritocli.items.remove(carritoprod)
        carritoprod.delete()
    else:
        carritoprod.cantidad -= 1
        carritoprod.save()
    return redirect(to='carrito')

def carrito(request):
    carritocli = CarritoCliente.objects.get(usuario = request.user)
    productos_carrito = carritocli.items.all()
    precio_total = carritocli.calcular_total()
    data = {
        'productos': productos_carrito,
        'total': precio_total,
    }
    return render(request, 'core/carrito.html',data)

def borrar_carrito(request, id):
    producto = Producto.objects.get(id=id)
    carritocli = CarritoCliente.objects.get(usuario=request.user)
    carritoprod = CarritoProducto.items.get(producto=producto)

    carritocli.items.remove(carritoprod)
    carritoprod.delete()

    return redirect(to='carrito')
# CIERRE VIEWS DEL CARRITO

def perfilusuario(request):
    usuariosAll = User.objects.all()
    data = {
        'listadoUser' : usuariosAll
    }
    return render(request,'core/perfilusuario.html',data)

def boleta(request):
    return render(request,'core/boleta.html')

def index(request):
    productosAll = Producto.objects.all()
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    try:
        paginator = Paginator(productosAll, 5)
        productosAll = paginator.page(page)
    except:
        raise Http404
    data = {
        'listado': productosAll,
        'paginator': paginator
    }
    return render(request,'core/index.html',data)

#Index cambia por Productos dependiendo donde lo pongamos, creo que podemos hacer uno para cada uno
#Crud
    
#FinCrud

#################################################################################################################
def agregar(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST': 
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save() #COMMIT
            #data['msj'] = 'Producto guardado correctamente!'
            messages.success(request, "Producto almacenado correctamente")
    return render(request,'core/agregar.html',data)

def modificar(request,id):
    producto = Producto.objects.get(id=id)
    data = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method =='POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) 
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto actualizado correctamente")
            data['form'] = formulario
    return render(request, 'core/modificar.html',data)

def delete(request,id):
    producto = Producto.objects.get(id=id) # BUSCAMOS UN PRODUCTO POR SU ID
    producto.delete()

    return redirect(to="index")
##############################################################
def registrarse(request):
    data = {
        'form' : UsuarioForm()
    }
    if request.method == 'POST': 
        formulario = UsuarioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save() #COMMIT
            #data['msj'] = 'Producto guardado correctamente!'
            messages.success(request, "Producto almacenado correctamente")
    return render(request,'core/registrarse.html',data)
