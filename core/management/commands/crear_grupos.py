"""Crea los 3 grupos del ERP: Gerente, Vendedor, Almacen.

Uso: python manage.py crear_grupos
"""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

APPS_ERP = ['clientes', 'proveedores', 'productos', 'ventas', 'configuracion']


def perms(app_models, acciones):
    """app_models: lista de (app_label, model_name). Devuelve Permission."""
    codenames = {(a, f'{ac}_{m}') for a, m in app_models for ac in acciones}
    ids = []
    for app, code in codenames:
        ids += list(Permission.objects.filter(
            content_type__app_label=app, codename=code
        ).values_list('pk', flat=True))
    return Permission.objects.filter(pk__in=ids)


class Command(BaseCommand):
    help = 'Crea o actualiza los grupos Gerente, Vendedor y Almacen'

    def handle(self, *args, **options):
        # Gerente: todo en las apps del ERP
        gerente, c1 = Group.objects.get_or_create(name='Gerente')
        pg = Permission.objects.filter(content_type__app_label__in=APPS_ERP)
        gerente.permissions.set(pg)

        vendedor, c2 = Group.objects.get_or_create(name='Vendedor')
        pv = (perms([('ventas', 'venta'), ('ventas', 'detalleventa')],
                    ('add', 'view'))
              | perms([('productos', 'producto'), ('clientes', 'cliente')],
                      ('view',)))
        vendedor.permissions.set(pv)

        almacen, c3 = Group.objects.get_or_create(name='Almac\u00e9n')
        pa = (perms([('productos', 'producto'), ('productos', 'categoria')],
                    ('add', 'change', 'view'))
              | perms([('proveedores', 'proveedor')], ('view',)))
        almacen.permissions.set(pa)

        for g, c, n in ((gerente, c1, pg.count()), (vendedor, c2, pv.count()),
                        (almacen, c3, pa.count())):
            self.stdout.write(self.style.SUCCESS(
                f'{g.name}: {n} permisos ({"creado" if c else "actualizado"})'))
