
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
            return redirect('menu')  # Redirige a una vista que liste los artículos
        else:
            print(form.errors)  # Muestra los errores de validación en la consola
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
    graphql_url = 'http://localhost:8000/graphql/'
    
  # Obtener los parámetros de la solicitud
    category = request.GET.get('category')
    author = request.GET.get('author')
    date = request.GET.get('date')

    # Crear la consulta básica para obtener artículos
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

    # Modificar la consulta si se proporciona una categoría
    if category:
        query = f"""
        query {{
            allArticles(category: "{category}") {{
                id
                title
                content
                category
                author
                publishedDate
            }}
        }}
        """

    # Modificar la consulta si se proporciona un autor
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

    # Modificar la consulta si se proporciona una fecha
    if date:
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

    # Realiza la petición POST al servidor GraphQL
    response = requests.post(graphql_url, json={'query': query})

    # Verificar el contenido de la respuesta del servidor
    print("Contenido de la respuesta:", response.text)

    try:
        articles = response.json().get('data', {}).get('allArticles', [])
        print("Artículos obtenidos:", articles)
    except json.JSONDecodeError:
        return render(request, 'menu.html', {'error': 'Error al decodificar la respuesta del servidor GraphQL', 'response': response.text})

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
