"""
URL configuration for dj_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from book_shelf.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ManufacturerAPI, WarehouseAPI, ProductAPI
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register('manufacturers', ManufacturerAPI, basename='manufacturers')
router.register('warehouses', WarehouseAPI, basename='warehouses')
router.register('products', ProductAPI, basename='products')

urlpatterns = [
                  path('', ProductListView.as_view(), name='product_list'),
                  path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
                  path('create/', ProductCreateView.as_view(), name='product_create'),
                  path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
                  path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
                  path('admin/', admin.site.urls),
                  path('schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
              ] + router.urls
