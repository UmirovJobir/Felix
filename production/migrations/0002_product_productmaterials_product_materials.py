# Generated by Django 5.0.3 on 2024-03-19 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('code', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='materials',
            field=models.ManyToManyField(through='production.ProductMaterials', to='production.material'),
        ),
    ]
