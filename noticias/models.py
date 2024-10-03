from django.db import models

class Article(models.Model):
    CATEGORY_CHOICES = [
    ('politica', 'Política'),
    ('deportes', 'Deportes'),
    ('tecnologia', 'Tecnología'),
    ('salud', 'Salud'),
]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  # Cambiado a opciones
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
