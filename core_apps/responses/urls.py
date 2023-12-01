from django.urls import path
from .views import ResponseUpdateDeleteView, ResposeListCreateView

urlpatterns = [
    path("article/<uuid:article_id>/", ResposeListCreateView.as_view(), name="article_reponses"),
    path("<uuid:id>/", ResponseUpdateDeleteView.as_view(), name="response_detail")

]
