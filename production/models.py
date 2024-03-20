from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=225)
    code = models.CharField(max_length=500)
    materials = models.ManyToManyField(Material, through='ProductMaterials')

    def __str__(self):
        return self.name


class ProductMaterials(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Warehouse(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

