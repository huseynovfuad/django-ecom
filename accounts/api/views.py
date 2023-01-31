from rest_framework import generics
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from accounts.models import MyUser as User
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)

        token = RefreshToken.for_user(user)

        data = {
            **serializer.data,
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return Response(data, status=201)



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=True)

        return Response(serializer.data, status=201)