from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        exclude = ["id"]
        read_only_fields = (
            "public_id",
            "created_at",
            "updated_at",
        )
