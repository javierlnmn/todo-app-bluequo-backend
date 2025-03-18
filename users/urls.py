from django.urls import path

from .views import (
    SignupView,
    LoginView,
    TestTokenView,
)

app_name='users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/test/', TestTokenView.as_view(), name='test-token'),
]
