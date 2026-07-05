from django.urls import path
from .views import SourceAPIView, KnowledgeBaseAPIView

urlpatterns = [
    path('sources/', SourceAPIView.as_view(), name='source-list-create'),
    path('knowledge-bases/', KnowledgeBaseAPIView.as_view(), name='knowledgebase-list-create'),
]
