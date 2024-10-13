import django_filters
from .models import Photo

class PhotoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    photographer = django_filters.CharFilter(field_name='photographer__username', lookup_expr='icontains')  # Correct field reference for username
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Created At (From)')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Created At (To)')

    class Meta:
        model = Photo
        fields = ['title', 'photographer', 'category', 'tags', 'created_at__gte', 'created_at__lte']
