from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import Subscription, User
from users.serializer import CheckSubscribeSerializer, SubscribeSerializer


class SubscribeAPIView(APIView):
    '''
    CRUD подписок
    '''

    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        serializer = SubscribeSerializer(
            data=dict(user=request.user.id, author=id),
            context=dict(request=request)
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Subscription.objects.filter(user=request.user,
                                    author_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckSubscribeAPIView(ListAPIView):
    '''
    Показать подписки
    '''

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = User.objects.filter(
            user__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = CheckSubscribeSerializer(
            page, many=True, context=dict(request=request)
        )
        return self.get_paginated_response(serializer.data)
