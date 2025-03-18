from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    TodoViewSet,
    CommentViewSet
)


app_name = 'todos'

router = DefaultRouter()

router.register(r'todos', TodoViewSet,)
router.register(r'comments', CommentViewSet,)

urlpatterns = [
    path('', include(router.urls)),
]
