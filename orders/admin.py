from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe


# Register your models here.

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # zapis pierwszego rekordu wraz z informacjami nagłowka
    writer.writerow([field.verbose_name for field in fields])
    # zapis rekordow danych
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Eksport do CSV'

def order_detail(obj):
    return mark_safe('<a href="{}">Szczegóły</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])
    ))



class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail]
    list_filter = ['created', 'updated', 'paid']
    inlines = [OrderItemInLine]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)

