from django.urls import path

from .views import ContactListView, ContactUpdateView

urlpatterns = [
    path("contacts/", ContactListView.as_view(), name="contact-list"),
    path("contacts/<int:pk>/", ContactUpdateView.as_view(), name="contact-update"),
]
