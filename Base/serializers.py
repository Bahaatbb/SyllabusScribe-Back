from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (LessonContext, LessonHandout, LessonPlan,
                     LessonPresentation, LessonQuiz, QuizQA, Subject, User)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'bio', 'avatar']

    def create(self, validated_data):
        default_avatar = User._meta.get_field('avatar').get_default()
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'].lower(),
            bio=validated_data.get('bio', None),
            avatar=validated_data.get('avatar', default_avatar)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'date_joined', 'email', 'bio', 'avatar']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ['user']


class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        exclude = ['user']


class LessonContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContext
        exclude = ['user']


class LessonPresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPresentation
        exclude = ['user']


class LessonHandoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHandout
        exclude = ['user']


class LessonQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonQuiz
        exclude = ['user']


class QuizQASerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQA
        exclude = ['lesson_quiz']
