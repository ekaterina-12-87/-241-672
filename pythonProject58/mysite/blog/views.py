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


# Create your views here.
