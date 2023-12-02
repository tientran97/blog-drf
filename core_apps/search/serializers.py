from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

#from core_apps.search import documents

from .documents import ArticleDocument


class ArticleElasticSearchSerializer(DocumentSerializer):
    class Meta:
        documents = ArticleDocument
        fields = ["title", "author", "slug", "description", "body", "created_at"]
