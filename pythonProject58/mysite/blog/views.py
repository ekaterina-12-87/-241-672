'''
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q
from django.http import Http404
from .models import Hotel, Room, Booking, Client

from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, 'blog/404.html', status=404)


def post_list(request):
    print("Post list view called!")
    try:
        # Виджет 1: Отели с доступными номерами
        hotels_with_rooms = Hotel.objects.annotate(
            available_rooms=Count('room', filter=Q(room__availability='доступен'))
        ).filter(available_rooms__gt=0).order_by('-stars')[:3]

        # Виджет 2: Последние бронирования есть ли здесь противоречия с более ранними кодами
        recent_bookings = Booking.objects.select_related(
            'client', 'room', 'room__hotel'
        ).order_by('-arrival_date')[:5]

        # Виджет 3: Статистика
        stats = {
            'total_hotels': Hotel.objects.count(),
            'available_rooms': Room.objects.filter(availability='доступен').count(),
            'avg_price': Room.objects.aggregate(avg=Avg('price_day'))['avg'],
        }

        context = {
            'hotels': hotels_with_rooms,
            'bookings': recent_bookings,
            'stats': stats,
        }
        return render(request, 'blog/post/list.html', context)

    except Exception as e:
        raise Http404("Ошибка загрузки данных") from e


def post_detailo(request, pk):
    # Используем get_object_or_404 для обработки несуществующих номеров
    room = get_object_or_404(
        Room.objects.select_related('hotel'),
        pk=pk,
        availability='доступен'  # Дополнительная проверка доступности
    )

    # Расчет стоимости с обработкой ошибок
    def calculate_price(room, days, has_pet=False):
        try:
            base_price = room.price_day * days
            cleaning_fee = room.cleaning_fee if has_pet and room.pet_friendly == 'Разрешено' else 0
            return base_price + cleaning_fee
        except (TypeError, ValueError):
            return room.price_day  # Возвращаем цену за 1 день при ошибке

    context = {
        'room': room,
        'calculate_price': calculate_price,
    }
    return render(request, 'blog/post/detailo.html', context)
'''

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



# views.py
from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min, Sum
from .models import Hotel, Room, Booking, Client
from django.contrib.postgres.search import SearchVector


def home_view(request):
    # Статистика (агрегатные функции)
    stats = {
        'total_hotels': Hotel.objects.count(),
        'available_rooms': Room.objects.filter(availability='доступен').count(),
        'avg_price': Room.objects.aggregate(avg=Avg('price_day'))['avg'],
        'max_price': Room.objects.aggregate(max=Max('price_day'))['max'],
        'min_price': Room.objects.aggregate(min=Min('price_day'))['min'],
    }

    top_hotels = Hotel.objects.annotate(
        bookings_count=Count('room__booking')
    ).order_by('-bookings_count')[:5]

    recent_bookings = Booking.objects.select_related(
        'client', 'room', 'room__hotel'
    ).order_by('-arrival_date')[:5]

    # Доступные номера с изображениями
    available_rooms = Room.objects.filter(
        availability='доступен'
    ).select_related('hotel').order_by('?')[:10]

    # Поиск
    search_results = []
    search_query = ''

    if request.method == 'GET' and 'search' in request.GET:
        search_query = request.GET.get('search', '')
        search_results = Room.objects.annotate(
            search=SearchVector('hotel__name', 'type', 'hotel__location__city')
        ).filter(search=search_query)

    context = {
        'stats': stats,
        'top_hotels': top_hotels,
        'recent_bookings': recent_bookings,
        'available_rooms': available_rooms,
        'search_results': search_results,
        'search_query': search_query,
    }
    return render(request, 'blog/post/list.html', context)

from django.shortcuts import render, get_object_or_404

def room_detail(request, room_id):
    room = get_object_or_404(Room.objects.select_related('hotel'), id=room_id)
    return render(request, 'blog/detailo.html', {'room': room})

# views.py
from django.http import FileResponse
from django.conf import settings

def test_image(request):
    return FileResponse(open(os.path.join(settings.MEDIA_ROOT, 'room_images/test.jpg'), 'rb'))


def hotel_detail(request, hotel_id):
    try:
        hotel = Hotel.objects.prefetch_related('room_set').get(id=hotel_id)
    except Hotel.DoesNotExist:
        return render(request, 'blog/404.html', status=404)

    stats = {
        'total_rooms': hotel.room_set.count(),
        'available_rooms': hotel.room_set.filter(availability='доступен').count(),
        'avg_price': hotel.room_set.aggregate(avg=Avg('price_day'))['avg'],
    }

    recent_bookings = Booking.objects.filter(
        room__hotel=hotel
    ).select_related('client', 'room').order_by('-arrival_date')[:5]

    return render(request, 'blog/post/hotel_detail.html', {
        'hotel': hotel,
        'stats': stats,
        'recent_bookings': recent_bookings,
        'rooms': hotel.room_set.all()
    })


def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related('client', 'room', 'room__hotel', 'pet'),
        id=booking_id
    )
    return render(request, 'blog/post/booking_detail.html', {'booking': booking})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm


def booking_add(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'действительно'  # Устанавливаем статус по умолчанию
            booking.save()
            messages.success(request, f'Бронирование #{booking.id} успешно создано!')
            return redirect('blog:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'blog/post/booking_form.html', {
        'form': form,
        'title': 'Создание бронирования',
        'btn_text': 'Создать',
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking


def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            messages.success(request, f'Бронирование #{booking.id} успешно обновлено!')
            return redirect('blog:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'blog/post/booking_form.html', {
        'form': form,
        'title': f'Редактирование бронирования #{booking.id}',
        'btn_text': 'Сохранить',
    })


def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'Бронирование #{booking_id} успешно удалено!')
        return redirect('blog:booking_list')

    return render(request, 'blog/post/booking_confirm_delete.html', {'booking': booking})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking
from .forms import BookingForm

def booking_list(request):
    bookings = Booking.objects.select_related('client', 'room', 'room__hotel').order_by('-arrival_date')
    return render(request, 'blog/post/booking_list.html', {'bookings': bookings})

# Остальные представления (booking_detail, booking_add, booking_edit, booking_delete) остаются без изменений