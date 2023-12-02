from django.urls import path

from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
    LikeArticleView,
)

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article-list_create"),
    path(
        "<uuid:id>/",
        ArticleRetrieveUpdateDestroyView.as_view(),
        name="article-retrieve-update-destroy",
    ),
    path("<uuid:article_id>/like/", LikeArticleView.as_view(), name="like-article"),
]
