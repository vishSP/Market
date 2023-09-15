# Generated by Django 4.2.5 on 2023-09-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='наименование')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateField(verbose_name='дата последнего изменения ')),
                ('is_active', models.BooleanField(default=False, verbose_name='признак публикации')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('name',),
            },
        ),
    ]
