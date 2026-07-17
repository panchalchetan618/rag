from django.db import models
from pgvector.django import VectorField
from shared.models import BaseModel


class KnowledgeBase(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Source(BaseModel):
    SOURCE_CHOICES = (
        ("pdf", "PDF"),
        ("docx", "DOCX"),
        ("txt", "Text"),
        ("md", "Markdown"),
        ("html", "HTML"),
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    name = models.CharField(max_length=255)
    source_url = models.URLField(blank=True, null=True)
    source_file = models.FileField(upload_to="sources/", blank=True, null=True)
    source_type = models.CharField(
        max_length=10, choices=SOURCE_CHOICES, null=True, blank=True
    )
    file_size = models.BigIntegerField(null=True, blank=True)
    file_signature = models.CharField(
        max_length=64, null=True, blank=True, db_index=True
    )
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    page_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    update_frequency_in_days = models.PositiveIntegerField(default=0)
    knowledge_base = models.ForeignKey(
        KnowledgeBase, on_delete=models.CASCADE, related_name="sources", db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    (
                        models.Q(source_url__isnull=False)
                        & models.Q(source_file__isnull=True)
                    )
                    | (
                        models.Q(source_url__isnull=True)
                        & models.Q(source_file__isnull=False)
                    )
                ),
                name="source_url_xor_file",
            )
        ]


class DocumentChunk(BaseModel):
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    chunk_index = models.PositiveIntegerField()
    content = models.TextField()
    embedding = VectorField(dimensions=768)
    page_number = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    metadata = models.JSONField(default=dict)
