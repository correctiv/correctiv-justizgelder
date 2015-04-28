from django.contrib import admin

from .models import Fine, Organisation


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'sum_fines', 'treasury')
    list_filter = ('treasury',)
    search_fields = ['name']


class FineAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'state', 'year', 'department', 'department_detail', 'treasury')
    list_filter = ('state', 'department', 'year', 'treasury')
    search_fields = ['original_name', 'department_detail']
    raw_id_fields = ('organisation',)


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Fine, FineAdmin)
