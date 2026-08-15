from django.contrib import admin

from core.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
