from django.urls import path

from .views import MessageListView

urlpatterns = [
    path("contacts/<int:contact_id>/messages/", MessageListView.as_view(), name="message-list"),
]
