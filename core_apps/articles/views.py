import logging
from django.http import  Http404
from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Article, ArticleView, Like
from .serializers import ArticleSerializer, LikeSerializer
from .filters import ArticleFilter
from .pagination import ArticlePagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

User = get_user_model()

logger = logging.getLogger(__name__)

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePagination
    filter_backends = ( DjangoFilterBackend, filters.OrderingFilter, )
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "updated_at"]
    renderer_classes = [ArticlesJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"article {serializer.data.get('title')} created by {self.request.user.first_name}") # type: ignore


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [ArticleJSONRenderer]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)

        ArticleView.record_view(article=instance, user=request.user, viewer_ip=viewer_ip)

        return Response(serializer.data)


class LikeArticleView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        if Like.objects.filter(user=user, article=article).exists():
            return Response(
                {"detail": "You have already like this article"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like = Like.objects.create(user=user, article=article)
        like.save()

        return Response(
            {"detail": "Liked article!"},
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        like = get_object_or_404(Like, user=user, article=article)
        like.delete()
        return Response(
            {"detail": "Removed like"},
            status=status.HTTP_204_NO_CONTENT
        )
