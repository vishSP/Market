from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    price = models.IntegerField(verbose_name='цена')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата последнего изменения ')

    is_active = models.BooleanField(default=False, verbose_name='признак публикации')

    def __str__(self):
        return f'{self.name}{self.price}'

    def delete(self, *args, **kwargs):
        self.save()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('name',)
