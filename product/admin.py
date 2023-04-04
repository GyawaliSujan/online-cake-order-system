from django.contrib import admin
from product.models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "order", "featured", "carousel")
    exclude = ("slug",)


class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cake_image', 'price', 'minsize', 'best_selling', 'categoriess')
    search_fields = ('name', 'categories__name')
    view_on_site = True
    actions = ['make_best_selling']

    def cake_image(self, obj):
        if not obj.image:
            return ""
        return format_html("<img src={} height=40 width=40/>".format(obj.image.url))

    def categoriess(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    def make_best_selling(self, request, queryset):
        queryset.update(best_selling=True)
    make_best_selling.short_description = 'Change status of selected Cakes to Best Selling'



class CakeFlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'additional_price_per_pound')


class CakeShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'additional_price_per_pound')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('client', 'items_list', 'payment_method', 'colored_status', 'delivery_time', 'created_on', 'delivery_location',
                    'receiver', 'secondary_receiver', 'message')
    date_hierarchy = 'delivery_time'
    filter_horizontal = ['items']
    list_filter = ('delivery_time', 'payment_method__method',
                   ('client', admin.RelatedOnlyFieldListFilter),)
    list_display_links = None
    inlines = (CartItemInline, )
    actions = ['make_pending', 'make_verified',
               'make_delivered', 'make_rejected']

    search_fields = ['payment_method__reference_code', 'client__first_name',
                     'client__last_name', 'delivery_location__location']

    def make_verified(self, request, queryset):
        queryset.update(status='verified')
    make_verified.short_description = 'Change status of selected items to verified'

    def make_pending(self, request, queryset):
        queryset.update(status='pending')
    make_pending.short_description = 'Change status of selected items to pending'

    def make_delivered(self, request, queryset):
        queryset.update(status='delivered')
    make_delivered.short_description = 'Change status of selected items to delivered'

    def make_rejected(self, request, queryset):
        queryset.update(status='rejected')
    make_rejected.short_description = 'Change status of selected items to rejected'


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'remark')
    date_hierarchy = 'date'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Cake, CakeAdmin)
admin.site.register(CakeShape, CakeShapeAdmin)
admin.site.register(CakeFlavor, CakeFlavorAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Holiday, HolidayAdmin)

# This is on purpose, we should avoid easy deletions
admin.site.disable_action('delete_selected')
