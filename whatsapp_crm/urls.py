from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Callback cru da Evolution API (não confundir com /api/, que é o que o
    # front-end consome)
    path("webhook/", include("apps.integrations.evolution.urls")),
    # API consumida pelo front-end (login, contatos, mensagens, status, envio manual)
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.contacts.urls")),
    path("api/", include("apps.conversations.urls")),
    path("api/", include("apps.integrations.evolution.api_urls")),
]
