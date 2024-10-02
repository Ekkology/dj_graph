
from django.shortcuts import render, redirect
from .form import ArticleForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirige a una vista que liste los artículos
    else:
        form = ArticleForm()
    
    return render(request, 'vista_inicial.html', {'form': form})



from django.contrib.auth import authenticate, login as auth_login  # Evitar conflictos con el nombre
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    return render(request, 'menu.html')


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
