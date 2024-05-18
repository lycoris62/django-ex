from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
  # 글 조회는 누구나, 생성은 로그인한 유저, 편집은 글 작성자
  def has_permission(self, request, view):  # 전체 객체 권한
    if request.method == "GET":
      return True
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):  # 각 객체별 권한
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.author == request.user
