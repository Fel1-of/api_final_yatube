from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Group, Comment, Follow, User


class UserSlugField(serializers.SlugRelatedField):
    """
    Расширенный SlugRelatedField, который превращает 500-ю ошибку
    (ObjectDoesNotExist) в 400 с понятным сообщением.
    """
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Пользователь не существует')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('id', 'author', 'post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = UserSlugField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = UserSlugField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны!'
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Невозможно оформить подписку на самого себя.'
            )
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return value
