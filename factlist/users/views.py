from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSignupSerializer, UserMeSerializer, UserAuthSerializer


class UserSignupView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSignupSerializer


class UserMeView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object


class UserLoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(UserMeSerializer(user).data)
