from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from shared.utils.response import success_response, error_response

from uuid import UUID

from .serializers import SourceSerializer, KnowledgeBaseSerializer
from .models import Source, KnowledgeBase


class SourceAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = SourceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    status.HTTP_201_CREATED,
                    "Source created successfully",
                    serializer.data,
                )
            return error_response(
                status.HTTP_400_BAD_REQUEST, "Validation failed", serializer.errors
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def get(self, request):
        try:
            kb_id = request.query_params.get("kb_id")
            source_id = request.query_params.get("source_id")

            if source_id:
                source = get_object_or_404(
                    Source, knowledge_base__id=kb_id, public_id=source_id
                )
                serializer = SourceSerializer(source)
            else:
                queryset = Source.objects.filter(knowledge_base__id=kb_id)

                is_active = request.query_params.get("is_active")
                if is_active is not None:
                    queryset = queryset.filter(is_active=is_active.lower() == "true")

                search = request.query_params.get("search")
                if search:
                    queryset = queryset.filter(name__icontains=search)

                created_after = request.query_params.get("created_after")
                if created_after:
                    queryset = queryset.filter(created_at__gte=created_after)

                created_before = request.query_params.get("created_before")
                if created_before:
                    queryset = queryset.filter(created_at__lte=created_before)

                serializer = SourceSerializer(queryset, many=True)

            return success_response(
                status.HTTP_200_OK,
                "Sources retrieved successfully",
                serializer.data,
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def patch(self, request):
        try:
            kb_id = request.query_params.get("kb_id")
            source_id = request.query_params.get("source_id")
            source = get_object_or_404(
                Source, knowledge_base__id=kb_id, public_id=source_id
            )
            serializer = SourceSerializer(source, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    status.HTTP_200_OK,
                    "Source updated successfully",
                    serializer.data,
                )
            return error_response(
                status.HTTP_400_BAD_REQUEST, "Validation failed", serializer.errors
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def delete(self, request):
        try:
            kb_id = request.query_params.get("kb_id")
            source_id = request.query_params.get("source_id")
            source = get_object_or_404(
                Source, knowledge_base__id=kb_id, public_id=source_id
            )
            source.delete()
            return success_response(
                status.HTTP_200_OK,
                "Source deleted successfully",
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )


class KnowledgeBaseAPIView(APIView):
    def post(self, request):
        try:
            serializer = KnowledgeBaseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    status.HTTP_201_CREATED,
                    "Knowledge base created successfully",
                    serializer.data,
                )
            return error_response(
                status.HTTP_400_BAD_REQUEST, "Validation failed", serializer.errors
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def get(self, request, public_id: UUID | None = None):
        try:
            if public_id:
                kb = get_object_or_404(KnowledgeBase, public_id=public_id)
                serializer = KnowledgeBaseSerializer(kb)
            else:
                queryset = KnowledgeBase.objects.all()
                search = request.query_params.get("search")
                if search:
                    queryset = queryset.filter(name__icontains=search)
                serializer = KnowledgeBaseSerializer(queryset, many=True)

            return success_response(
                status.HTTP_200_OK,
                "Knowledge bases retrieved successfully",
                serializer.data,
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def patch(self, request, public_id: UUID):
        try:
            kb = get_object_or_404(
                KnowledgeBase, public_id=public_id, user=request.user
            )
            serializer = KnowledgeBaseSerializer(kb, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    status.HTTP_200_OK,
                    "Knowledge base updated successfully",
                    serializer.data,
                )
            return error_response(
                status.HTTP_400_BAD_REQUEST, "Validation failed", serializer.errors
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )

    def delete(self, request, public_id: UUID):
        try:
            kb = get_object_or_404(
                KnowledgeBase, public_id=public_id, user=request.user
            )
            kb.delete()
            return success_response(
                status.HTTP_200_OK,
                "Knowledge base deleted successfully",
            )
        except Exception as e:
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                {type(e).__name__: str(e)},
            )
