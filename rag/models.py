from django.db import models
from shared.models import BaseModel


class KnowledgeBase(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Source(BaseModel):
    name = models.CharField(max_length=255)
    source_url = models.URLField(blank=True, null=True)
    source_file = models.FileField(upload_to="sources/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    update_frequency_in_days = models.PositiveIntegerField(default=0)
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE, related_name='sources')

    def __str__(self):
        return self.name
