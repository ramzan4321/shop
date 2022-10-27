from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, DestroyAPIView, ListCreateAPIView,RetrieveAPIView,UpdateAPIView
from .models import Category, Product
from .serializers import AddCategorySerializer, AddProductSerializer, UpdateAddProductCategory
from rest_framework.views import APIView


# Create your views here.
def index(request):
    return HttpResponse({'msg':'Welcome'})

class AddCategoryView(ListCreateAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = AddCategorySerializer

    def post(self, request, *args, **kwargs):
        if 'order' in request.data:
            
            if Category.objects.filter(order = request.data['order']).exists():
                to_update = Category.objects.all().values('id')
                
                for update in to_update:
                    query = Category.objects.get(id = update['id'])
                    if query.order is not None:
                        if query.order >= int(request.data['order']):
                            query.order = query.order+1
                            query.save()
        serializer = AddCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Category Added'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


class CategoryView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = AddCategorySerializer

class AddProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer

class ProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer

#--- POST /products/<product_id>/categories/<category_id>add the given product to the givencategory---#

class AddUpdateProductView(APIView):
    def post(self, request, *args, **kwargs):
        prod_id = self.kwargs['pk']
        cate_id = self.kwargs['id']
        cate_dict = [{'category': cate_id}]
        prod = Product.objects.get(id=prod_id)
        get_cate = Product.objects.filter(id=prod_id).values('category')
        list_cate = []
        for cate in get_cate:
            list_cate.append(cate)
        data = list_cate + cate_dict
        newlist = [d['category'] for d in data]
        newDict = {'category':newlist}
        serializer = UpdateAddProductCategory(prod,data=newDict,partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Product Category Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

#------------- Delete category------------------

class DeleteCate(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = AddCategorySerializer