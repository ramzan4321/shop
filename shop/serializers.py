from turtle import title
from unicodedata import category
from .models import Category,Product
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework_recursive.fields import RecursiveField
# Create your tests here.

class AddCategorySerializer(serializers.ModelSerializer):
    category = RecursiveField(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('id','title','parent','category','order')
    def validate(self, data):
        if Category.objects.filter(title=data['title'],parent=data['parent']):
            raise ValidationError('This Category is already exist !', HTTP_406_NOT_ACCEPTABLE)
        return data

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        cate = data['category']
        for cat in cate:
            if Category.objects.filter(title=cat,parent__isnull=True):
                raise ValidationError('Product could not be added in root category !', HTTP_406_NOT_ACCEPTABLE)
        if Product.objects.filter(name=data['name']):
            raise ValidationError('Product with this name already exist !', HTTP_406_NOT_ACCEPTABLE)
        if data['price'] <= 0:
            raise ValidationError('Price should be positive and greater than 0 !', HTTP_406_NOT_ACCEPTABLE)
        return data

class UpdateAddProductCategory(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','category')

    '''def update(self, instance, validated_data):
        instance.category = validated_data.get('category',instance.category)
        return instance'''