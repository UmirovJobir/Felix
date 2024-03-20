from django.contrib import admin
from .models import (
    Material,
    Product,
    ProductMaterials,
    Warehouse,
)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductMaterials)
class ProductMaterialsAdmin(admin.ModelAdmin):
    pass


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'material_id', 'remainder', 'price']

