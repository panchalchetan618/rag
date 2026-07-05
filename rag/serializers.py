from rest_framework import serializers
from .models import Source, KnowledgeBase


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    sources = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = KnowledgeBase
        fields = "__all__"

    def get_sources(self, obj):
        sources = Source.objects.filter(knowledge_base=obj)
        return SourceSerializer(sources, many=True).data
