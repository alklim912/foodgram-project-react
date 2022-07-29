from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from rest_framework_simplejwt.tokens import SlidingToken

from . import permissions, serializers
from app import models
from users.models import User


class APIToken(APIView):

    def post(self, request):
        serializer = serializers.AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=serializer.validated_data['email'])
        if (user.check_password(serializer.validated_data['password'])
                and user.is_active):
            token = {'auth_token': str(SlidingToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class APILogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        SlidingToken(
            request.META.get('HTTP_AUTHORIZATION').split()[1]
        ).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(CreateModelMixin, GenericViewSet,
                  ListModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(serializers.MeUserSerializer(request.user).data)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = serializers.SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.validated_data['current_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = models.Follow.objects.filter(user=request.user)
        serializer = serializers.FollowSerializer(
            queryset, many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if models.Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = models.Follow.objects.create(user=user, author=author)
        serializer = serializers.FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = models.Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = serializers.SignUpSerializer
        return self.serializer_class


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.method_select(request, pk, models.Favorite)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.method_select(request, pk, models.Cart)

    def method_select(self, request, pk, model):
        if request.method == 'POST':
            return self.add_obj(model, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(model, request.user, pk)
        return None

    def add_obj(self, model, user, pk):
        if not model.objects.filter(user=user, recipe__id=pk).exists():
            recipe = get_object_or_404(models.Recipe, id=pk)
            model.objects.create(user=user, recipe=recipe)
            serializer = serializers.FollowRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепт уже добавлен'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = models.RecipeIngredients.objects.filter(
            recipe__cart__user=request.user).order_by(
                'ingredient__name').values_list(
                    'ingredient__name', 'ingredient__measurement_unit'
                ).annotate(amount_total=Sum('amount'))
        pdfmetrics.registerFont(
            TTFont('TNR', 'times.ttf', 'UTF-8')
        )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('TNR', size=16)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('TNR', size=14)
        height = 750
        for i, (name, unit, amount) in enumerate(ingredients, 1):
            page.drawString(75, height, (f'{i}. {name} - {amount} {unit}.'))
            height -= 25
        page.showPage()
        page.save()
        return response
