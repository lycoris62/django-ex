from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def HelloAPI(request):
  return Response("hello world!")
