from django.urls import include, path
from shop.views import AddCategoryView, AddProductView, CategoryView, DeleteCate, ProductView, AddUpdateProductView
from shop import views

urlpatterns = [
    path('', views.index , name='index'),
    path('api/addcategory', AddCategoryView.as_view()),
    path('api/category/<int:pk>', CategoryView.as_view()),
    path('api/delcategory/<int:pk>', DeleteCate.as_view()),
    path('api/addproduct', AddProductView.as_view()),
    path('api/product/<int:pk>', ProductView.as_view()),
    path('api/product/<int:pk>/category/<int:id>', AddUpdateProductView.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]