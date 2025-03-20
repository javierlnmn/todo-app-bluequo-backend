from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SignupView,
    LoginView,
    TestTokenView,
    UserViewSet
)


app_name='users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/test/', TestTokenView.as_view(), name='test-token'),
]
