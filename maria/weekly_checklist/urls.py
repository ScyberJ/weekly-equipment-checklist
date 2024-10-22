from django.conf import settings
from django.urls import path
from django.contrib.auth.views import logout_then_login, LoginView
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *



urlpatterns = [
    path("", home, name='home'),
    path("logout", logout_then_login, name="logout"),
    path("login", LoginView.as_view(), name='login'),
    path("request-equipment", login_required(request_equipment), name="request-equipment"),
    path("equipment/<int:pk>/add-", login_required(add_equipment), name="add-equipment"),
    path("request/<str:pk>/remove-equipment", login_required(remove_equipment), name="remove-equipment"),
    path("request/<str:pk>/submit", login_required(submit_request), name="submit-request"),
    path("list-requests", login_required(list_requests), name="list-requests"),
    path("request/<str:pk>/fix", login_required(mark_as_done), name="fix-request"),
    path("request/<str:pk>", login_required(request_detail), name="request-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
