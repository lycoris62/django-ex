from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password  # 장고 기본 비밀번호 검증
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator  # 이메일 중복 검증

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
      required=True,
      validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
      write_only=True,
      required=True,
      validators=[validate_password]
  )
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ('username', 'password', 'password2', 'email',)

  def validate(self, data):
    if data['password'] != data['password2']:
      raise serializers.ValidationError({
        "password": "Password fields didn't match."
      })
    return data

  def create(self, validated_data):
    # create 요청에 대해 오버라이딩하여 유저를 생성하고 토큰 생성
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email']
    )
    user.set_password(validated_data['password'])
    user.save()
    token = Token.objects.create(user=user)
    return user


class LoginSerializer(serializers.Serializer):  # 모델과 관련 없음, 사용자의 id,pw 받아서 그에 대한 토큰만 줌
  username = serializers.CharField(required=True)
  password = serializers.CharField(required=True, write_only=True)

  # write_only 옵션을 통해 클라->서버 방향의 역직렬화는 가능, 서버->클라는 불가능

  def validate(self, data):
    user = authenticate(**data)
    if user:
      token = Token.objects.get(user=user)
      return token
    raise serializers.ValidationError({
      "error": "Unable to login with provided credentials."
    })


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('nickname', 'position', 'subjects', 'image')
