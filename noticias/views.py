
from django.shortcuts import render, redirect
from .form import ArticleForm

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirige a una vista que liste los artículos
    else:
        form = ArticleForm()
    
    return render(request, 'vista_inicial.html', {'form': form})


def menu(request):
    return render(request,'menu.html')


def login(request):
    return render(request,'login.html')