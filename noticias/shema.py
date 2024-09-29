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
            articles = articles.filter(category=category)
        if author:
            articles = articles.filter(author=author)
        if date:
            articles = articles.filter(published_date__date=date)
        return articles

schema = graphene.Schema(query=Query)
