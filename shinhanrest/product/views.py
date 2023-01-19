from rest_framework import generics, mixins
from .models import Product

class ProductListView(mixins.ListModelMixin, generics.GenericAPIView):
    # serialize : 객체를 json으로 변환
    def serializer_class(self):
        pass

    def get_queryset(self):
        # GenericAPIView 가 가지는 메서드
        return Product.objects.all().order_by('id')

    # 리스트 전달, get: ListModelMixin이 가지는 메서드
    def get(self, request, *args, **kwargs):
        # Queryset
        # serializer_class
        # return Response
        return self.list(request, args, kwargs)