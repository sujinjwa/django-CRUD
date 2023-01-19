from rest_framework import status # 상태 코드 반환하기 위한 프레임워크
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product

class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):

        # 1. get 하기 전에 exists()로 확인하고 가져오기
        # 2. get 할 때 예외처리하기
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist: # 존재하지 않을 때에만 예외 처리
            return Response(status=status.HTTP_404_NOT_FOUND)
            

        # print(request.POST.get('name'))
        product = Product.objects.get(pk=pk)
        # print(product['name'])
        
        ret = {
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }

        return Response(ret)
    
    def delete(self, request, pk, *args, **kwargs):

        # 1. 없으면 지워졌다고 거짓말 하기(204 반환)
        # 2. 없으면 없다고 반환하기 (404 반환)
        if Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk, *args, **kwargs):
        # 수정할 Product 객체 가져오기
        product = Product.objects.get(pk=pk)

        # request.data에 데이터가 들어있었다
        # request.data에 모든 데이터가 있는 것은 아니다
        # 값을 수정할 때는 객체 안에 있는 변수의 값을 바꾸면 된다

        dirty = False # dirty : 수정된 값이 있는지 여부 확인
        for field, value in request.data.items():
            if field not in [f.name for f in product._meta.get_fields()]:
                continue
            # getattr : product의 field값 가져오기
            # getattr로 가져온 값과 value와 비교했을 때 다르다면 dirty는 True
            # 연산자 or로 묶여 있으니까 한 번이라도 다른 값이 나왔다면 dirty = True
            dirty = dirty or (value != getattr(product, field))
            setattr(product, field, value) # product 내 field 값을 value로 수정

        # if 'name' in request.data:
        #     product.name = request.data['name']
        
        # if 'price' in request.data:
        #     product.price = request.data['price']
        
        # if 'product_type' in request.data:
        #     product.product_type = request.data['product_type']
        
        # 값을 수정한 결과를 반영해야한다(save함수=create가 아닌 이미 존재하는 객체 update)
        if dirty: # 수정된 경우에만 save 함수 사용
            product.save()

        return Response(status=status.HTTP_206_PARTIAL_CONTENT)

class ProductListView(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.data['name'])

        # # Product 객체 생성
        # product = Product(
        #     name=request.data['name'],
        #     price=request.data['price'],
        #     product_type=request.data['product_type'],
        # )

        # # 객체의 save 함수 사용하여 Database 저장
        # product.save()

        # 전달한 값 받아오기
        name = request.data.get('name')
        price = request.data.get('price')
        product_type = request.data.get('product_type')

        # Product 객체 생성
        product = Product(
            name=name,
            price=price,
            product_type=product_type,
        )

        # 객체의 save 함수 사용하여 Database에 저장
        product.save() # Primary Key가 생성되는 시기!

        return Response({
            'id': product.id, # id 값을 넣어준다
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        # print(request.query_params)
        ret = []
        # QuerySet
        products = Product.objects.all()

        # price에 전달된 값보다 같거나 작은(__lte) 상품을 검색(filter)
        if 'price' in request.query_params:
            price = request.query_params['price']
            products = products.filter(price__lte=price)
        
        # name에 전달된 값이 포함된(__contains) 상품을 검색(filter)
        if 'name' in request.query_params:
            name = request.query_params['name']
            products = products.filter(name__contains=name)

        products = products.order_by('id')

        for product in products:
            ret.append({
                'id': product.id, # id값을 넣어준다
                'name': product.name,
                'price': product.price,
                'product_type': product.product_type,
            })
        
        return Response(ret)