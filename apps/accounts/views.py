from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    """
    POST /api/auth/login/  { "username": "...", "password": "..." }
    Sem autenticação prévia — é o próprio ponto de entrada.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Usuário ou senha inválidos"}, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class LogoutView(APIView):
    """POST /api/auth/logout/ — invalida o token atual."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"ok": True})


class MeView(APIView):
    """GET /api/auth/me/ — pra frontend confirmar se o token salvo ainda é válido."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username})
