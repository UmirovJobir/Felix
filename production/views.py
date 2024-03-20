from rest_framework import views, status, response
from .models import Product, Warehouse


class CalculateView(views.APIView):
    def post(self, request):
        products_data = request.data.get("products", [])

        if not products_data:
            return response.Response(
                {"message": "No products provided in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = []
        allocated_materials = {}

        for product_data in products_data:
            product_code = product_data.get("product_code")
            product_qty = product_data.get("product_qty")

            """Get product by code."""
            product = Product.objects.get(code=product_code)

            product_materials_info = []

            """Get product's related material from ProductMaterials."""
            for product_material in product.productmaterials_set.all():
                material = product_material.material
                material_qty = product_material.quantity

                required_qty = product_qty * material_qty

                """Get required materials from Warehouse."""
                warehouse_materials = Warehouse.objects.filter(
                    material_id=material
                ).order_by("remainder")

                for warehouse in warehouse_materials:
                    if material.name not in allocated_materials:
                        allocated_materials[material.name] = {}

                    if warehouse.id not in allocated_materials[material.name]:
                        allocated_materials[material.name][warehouse.id] = 0

                    """Switch to another warehouse_materials value because all quantities of material are booked."""
                    if (
                        material.name in allocated_materials and
                        warehouse.id in allocated_materials[material.name] and
                        allocated_materials[material.name][warehouse.id] == warehouse.remainder
                    ):
                        continue

                    elif (
                        material.name in allocated_materials and
                        warehouse.id in allocated_materials[material.name] and
                        allocated_materials[material.name][warehouse.id] < warehouse.remainder
                    ):
                        """if the amount of material from one warehouse is not fully booked, then divide the 
                            remaining reminder."""
                        warehouse.remainder -= allocated_materials[material.name][warehouse.id]

                    if required_qty <= warehouse.remainder:
                        product_materials_info.append(
                            {
                                "warehouse_id": warehouse.id,
                                "material_name": material.name,
                                "qty": required_qty,
                                "price": warehouse.price,
                            }
                        )
                        warehouse.remainder -= required_qty

                        allocated_materials[material.name][warehouse.id] += required_qty
                        required_qty = 0
                        break
                    else:
                        product_materials_info.append(
                            {
                                "warehouse_id": warehouse.id,
                                "material_name": material.name,
                                "qty": warehouse.remainder,
                                "price": warehouse.price,
                            }
                        )
                        required_qty -= warehouse.remainder

                        allocated_materials[material.name][warehouse.id] += warehouse.remainder

                if required_qty > 0:
                    product_materials_info.append(
                        {
                            "warehouse_id": None,
                            "material_name": material.name,
                            "qty": required_qty,
                            "price": None,
                        }
                    )

            product_info = {
                "product_name": product.name,
                "product_qty": product_qty,
                "product_materials": product_materials_info,
            }

            result.append(product_info)

        response_data = {"result": result}

        return response.Response(response_data, status=status.HTTP_200_OK)
