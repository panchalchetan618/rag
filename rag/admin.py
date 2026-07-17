from django.contrib import admin
from .models import Source, KnowledgeBase


class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ["name", "public_id", "created_at", "updated_at"]
    search_fields = ["name", "public_id"]
    fields = [
        "name",
        "public_id",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "public_id",
        "created_at",
        "updated_at",
    ]


class SourceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "knowledge_base",
        "is_active",
        "source_url",
        "created_at",
    ]
    search_fields = ["name", "public_id", "source_url"]
    list_filter = ["is_active", "knowledge_base", "update_frequency_in_days"]
    fields = [
        "name",
        "source_url",
        "source_file",
        "is_active",
        "update_frequency_in_days",
        "knowledge_base",
        "public_id",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "public_id",
        "created_at",
        "updated_at",
    ]


admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)
admin.site.register(Source, SourceAdmin)
