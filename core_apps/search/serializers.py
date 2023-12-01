from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument
from core_apps.search import documents

class ArticleElasticSearchSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = ["title", "author", "slug", "description", "body", "created_at"]
