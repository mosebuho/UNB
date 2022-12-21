from django.contrib import admin
from .models import Military, Comment


@admin.register(Military)
class MilitaryAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "writer", "view", "like")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("board", "parents", "content", "date", "writer")
