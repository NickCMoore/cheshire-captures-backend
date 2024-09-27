import django_filters
from .models import Photo

class PhotoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    photographer = django_filters.CharFilter(field_name='photographer__user__username', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Photo
        fields = ['title', 'photographer', 'category', 'tags']
