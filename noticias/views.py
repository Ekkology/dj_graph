
from django.shortcuts import render, redirect
from .form import ArticleForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirige a una vista que liste los artículos
    else:
        form = ArticleForm()
    
    return render(request, 'vista_inicial.html', {'form': form})



from django.contrib.auth import authenticate, login as auth_login  
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render

@csrf_exempt
@login_required


def menu(request):
    # URL de tu endpoint GraphQL
    graphql_url = 'http://localhost:8000/graphql/'

    # Obtener los parámetros de búsqueda
    author = request.GET.get('author', '').strip()
    date = request.GET.get('date', '').strip()

    # Construir la consulta GraphQL con parámetros opcionales
    if author:
        query = f"""
        query {{
            allArticles(author: "{author}") {{
                id
                title
                content
                category
                author
                publishedDate
            }}
        }}
        """
    elif date:
        query = f"""
        query {{
            allArticles(date: "{date}") {{
                id
                title
                content
                category
                author
                publishedDate
            }}
        }}
        """
    else:
        # Consulta para obtener todos los artículos si no hay parámetros
        query = """
        query {
            allArticles {
                id
                title
                content
                category
                author
                publishedDate
            }
        }
        """

    # Hacer la petición POST al servidor GraphQL
    response = requests.post(graphql_url, json={'query': query})

    # Verificar el contenido de la respuesta del servidor
    print("Contenido de la respuesta:", response.text)  # Esto te ayudará a depurar si el servidor está devolviendo la información

    try:
        # Parsear los datos de la respuesta
        articles = response.json().get('data', {}).get('allArticles', [])
        print("Artículos obtenidos:", articles)  # Verifica que los artículos se están obteniendo correctamente
    except json.JSONDecodeError:
        # Si ocurre un error de JSON, muestra el contenido
        return render(request, 'menu.html', {'error': 'Error al decodificar la respuesta del servidor GraphQL', 'response': response.text})

    # Verificar si hay artículos disponibles
    if not articles:
        print("No hay artículos disponibles")

    # Pasar los artículos al contexto de la plantilla
    return render(request, 'menu.html', {'articles': articles})


def login(request):  # Cambia el nombre de la vista
    form_login = AuthenticationForm()
    form_register = UserCreationForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            form_login = AuthenticationForm(data=request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)  # Usa el método auth_login
                    return redirect('menu')  # Redirige al menú

        elif form_type == 'register':
            form_register = UserCreationForm(request.POST)
            if form_register.is_valid():
                form_register.save()
                return redirect('login')  # Redirige al login después del registro

    return render(request, 'login_register.html', {
        'form_login': form_login,
        'form_register': form_register
    })
