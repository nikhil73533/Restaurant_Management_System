import django_filters
from .models import Food

class OrderFilter(django_filters.FilterSet):
    class Meta:
        models = Food
        fields = {'Food_Type'}
