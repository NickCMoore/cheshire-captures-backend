from django.contrib import admin
from .models import Photo, Tag, Like, Comment

admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Comment)
