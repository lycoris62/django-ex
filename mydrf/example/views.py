from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from example.models import Book
from example.serializers import BookSerializer


# Create your views here.
@api_view(['GET'])
def HelloAPI(request):
  return Response("hello world!")


@api_view(['GET', 'POST'])
def booksAPI(request):
  if request.method == 'GET':
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    serializer = BookSerializer(data=request.data)  # 외부에서 온 데이터를 역직렬화
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bookAPI(request, bid):
  book = get_object_or_404(Book, bid=bid)
  serializer = BookSerializer(book)
  return Response(serializer.data, status=status.HTTP_200_OK)

class BooksAPI(APIView):
  def get(self, request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  def post(self, request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
  def get(self, request, bid):
    book = get_object_or_404(Book, bid=bid)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)


class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  lookup_field = 'bid' # 기본 모델 pk 가 아닌, bid 를 pk 로 사용하고 있으니 lookup_field 로 사용

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)
