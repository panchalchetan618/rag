from shared.serializers import BaseModelSerializer
from .models import Source, KnowledgeBase


class SourceSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Source


class KnowledgeBaseSerializer(BaseModelSerializer):
    sources = SourceSerializer(
        many=True,
        read_only=True,
    )

    class Meta(BaseModelSerializer.Meta):
        model = KnowledgeBase
