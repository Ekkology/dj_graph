import graphene
from graphene_django.types import DjangoObjectType
from .models import Article

class ArticleType(DjangoObjectType):
    class Meta:
        model = Article

class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType, category=graphene.String(), author=graphene.String(), date=graphene.String())

    def resolve_all_articles(self, info, category=None, author=None, date=None):
        articles = Article.objects.all()
        if category:
            articles = articles.filter(category__icontains=category)  # Búsqueda insensible a mayúsculas/minúsculas
        if author:
            articles = articles.filter(author__icontains=author)  # Búsqueda insensible a mayúsculas/minúsculas
        if date:
            articles = articles.filter(published_date__exact=date)  # Comparación exacta de fecha
        return articles

schema = graphene.Schema(query=Query)
