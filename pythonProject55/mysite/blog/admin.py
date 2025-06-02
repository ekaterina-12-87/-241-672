from django.contrib import admin
from .models import *


class PetRequirementInline(admin.TabularInline):
    model = PetRequirement
    extra = 1
    raw_id_fields = ('pet', 'requirement')
    verbose_name = "Требование для питомца"
    verbose_name_plural = "Требования для питомцев"


class PetInline(admin.TabularInline):
    model = Pet
    extra = 1
    verbose_name = "Питомец"
    verbose_name_plural = "Питомцы"


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    verbose_name = "Комната"
    verbose_name_plural = "Комнаты"


class WarehouseInline(admin.TabularInline):
    model = Warehouse
    extra = 1
    verbose_name = "Склад"
    verbose_name_plural = "Склады"


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"


#@admin.register(Hotel)
#class HotelAdmin(admin.ModelAdmin):
#    list_display = ('name', 'stars', 'location_preview')
#    list_filter = ('stars',)
#    search_fields = ('name',)
#    inlines = [RoomInline, WarehouseInline]
#    readonly_fields = ('stars',)
#
#    @admin.display(description='Местоположение')
#    def location_preview(self, obj):
#        return f"{obj.location.get('city', '')}, {obj.location.get('address', '')}"

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'location_preview')
    list_filter = ('stars',)
    search_fields = ('name',)
    inlines = [RoomInline, WarehouseInline]

    # Добавляем stars в fieldsets или fields
    fieldsets = (
        (None, {
            'fields': ('name', 'stars', 'location')
        }),
    )

    @admin.display(description='Местоположение')
    def location_preview(self, obj):
        return f"{obj.location.get('city', '')}, {obj.location.get('address', '')}"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'hotel', 'type', 'availability', 'price_day', 'pet_friendly', 'image_preview')
    list_filter = ('hotel', 'type', 'availability', 'pet_friendly')
    search_fields = ('number', 'hotel__name')
    raw_id_fields = ('hotel',)
    list_display_links = ('number', 'hotel')
    date_hierarchy = None
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'

    fieldsets = (
        (None, {
            'fields': ('number', 'hotel', 'type', 'availability', 'price_day',
                       'capacity', 'pet_friendly', 'cleaning_fee', 'image')
        }),
    )

    #@admin.display(description="Превью изображения")
    #def image_preview(self, obj):
    #    if obj.image:
    #        from django.utils.html import format_html
    #        return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
    #    return "Нет изображения"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('hotel')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_preview', 'price_living', 'pets_count')
    search_fields = ('name',)
    inlines = [PetInline]
    list_filter = ('price_living',)

    @admin.display(description='Контактные данные')
    def contact_preview(self, obj):
        return f"{obj.contact_data.get('phone', '')}, {obj.contact_data.get('email', '')}"

    @admin.display(description='Питомцев')
    def pets_count(self, obj):
        return obj.pet_set.count()


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('type', 'owner', 'weight', 'requirements_count')
    list_filter = ('type',)
    search_fields = ('owner__name', 'type')
    raw_id_fields = ('owner',)
    inlines = [PetRequirementInline]

    @admin.display(description='Требований')
    def requirements_count(self, obj):
        return obj.petrequirement_set.count()


@admin.register(SpecialRequirement)
class SpecialRequirementAdmin(admin.ModelAdmin):
    list_display = ('category', 'short_description')
    list_filter = ('category',)
    search_fields = ('description', 'category')

    @admin.display(description='Описание')
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description


@admin.register(PetRequirement)
class PetRequirementAdmin(admin.ModelAdmin):
    list_display = ('pet', 'requirement', 'severity', 'short_notes')
    list_filter = ('severity', 'requirement__category')
    search_fields = ('pet__type', 'requirement__description')
    raw_id_fields = ('pet', 'requirement')

    @admin.display(description='Примечания')
    def short_notes(self, obj):
        return obj.notes[:50] + '...' if obj.notes and len(obj.notes) > 50 else obj.notes or '-'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'room', 'arrival_date', 'departure_date', 'status', 'duration_days')
    list_filter = ('status', 'arrival_date', 'room__hotel')
    search_fields = ('client__name', 'room__number')
    raw_id_fields = ('client', 'room', 'pet')
    date_hierarchy = 'arrival_date'

    @admin.display(description='Длительность (дни)')
    def duration_days(self, obj):
        return obj.duration


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'location_preview')
    list_filter = ('hotel',)
    search_fields = ('hotel__name',)
    inlines = [ProductInline]
    raw_id_fields = ('hotel',)

    @admin.display(description='Местоположение')
    def location_preview(self, obj):
        return obj.location.get('description', 'Не указано')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'price', 'warehouse', 'creator_short')
    list_filter = ('warehouse__hotel',)
    search_fields = ('name', 'creator')
    raw_id_fields = ('warehouse',)

    @admin.display(description='Производитель')
    def creator_short(self, obj):
        return obj.creator[:20] + '...' if len(obj.creator) > 20 else obj.creator


@admin.register(Require)
class RequireAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'required_count', 'hotel', 'client', 'request_date')
    list_filter = ('request_date', 'hotel')
    search_fields = ('product_name', 'client__name')
    raw_id_fields = ('product', 'hotel', 'client')
    date_hierarchy = 'request_date'







