from django.urls import path

from .api_views import InstanceQRCodeView, InstanceStatusView, SendMessageView

urlpatterns = [
    path("evolution/status/", InstanceStatusView.as_view(), name="evolution-status"),
    path("evolution/qrcode/", InstanceQRCodeView.as_view(), name="evolution-qrcode"),
    path("send-message/", SendMessageView.as_view(), name="send-message"),
]
