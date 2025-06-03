from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator

#class Hotel(models.Model):
#    name = models.CharField(max_length=25, verbose_name="Название отеля")
#    location = models.JSONField(verbose_name="Местоположение")
#    stars = models.IntegerField(
#        validators=[MinValueValidator(1), MaxValueValidator(5)],
#        verbose_name="Количество звезд"
#    )

class Hotel(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название отеля")
    location = models.JSONField(verbose_name="Местоположение")
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Количество звезд",
        default=3
    )

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.stars}*)"

class Room(models.Model):
    ROOM_TYPES = (
        ('Стандарт', 'Стандарт'),
        ('Комфорт', 'Комфорт'),
        ('Люкс', 'Люкс'),
    )
    AVAILABILITY = (
        ('доступен', 'Доступен'),
        ('недоступен', 'Недоступен'),
    )
    PET_POLICY = (
        ('Разрешено', 'Разрешено'),
        ('Запрещено', 'Запрещено'),
    )

    number = models.IntegerField(verbose_name="Номер комнаты")
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        verbose_name="Отель"
    )
    type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        verbose_name="Тип комнаты"
    )
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY,
        default='доступен',
        verbose_name="Доступность"
    )
    price_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за день"
    )
    capacity = models.IntegerField(verbose_name="Вместимость")
    pet_friendly = models.CharField(
        max_length=20,
        choices=PET_POLICY,
        verbose_name="Разрешены ли питомцы"
    )
    cleaning_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Плата за уборку"
    )

    #image = models.ImageField(
    #    upload_to='room_images/',
    #    verbose_name="Изображение номера",
    #    blank=True,
    #    null=True,
    #    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    #)
    image = models.ImageField(
        upload_to='room_images/',
        verbose_name="Изображение номера",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        unique_together = ('number', 'hotel')
        ordering = ['hotel', 'number']

    def __str__(self):
        return f"{self.hotel.name} - комната {self.number} ({self.type})"

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    contact_data = models.JSONField(verbose_name="Контактные данные")
    price_living = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость проживания"
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    def __str__(self):
        return self.name

class Pet(models.Model):
    PET_TYPES = (
        ('Собака', 'Собака'),
        ('Кошка', 'Кошка'),
        ('Птица', 'Птица'),
        ('Грызун', 'Грызун'),
        ('Другое', 'Другое'),
    )

    type = models.CharField(max_length=20, choices=PET_TYPES, verbose_name="Тип питомца")
    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Владелец"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Вес (кг)"
    )

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        ordering = ['owner', 'type']

    def __str__(self):
        return f"{self.type} ({self.owner.name})"

class SpecialRequirement(models.Model):
    CATEGORIES = (
        ('Медицинские', 'Медицинские'),
        ('Поведенческие', 'Поведенческие'),
        ('Диетические', 'Диетические'),
        ('Бытовые', 'Бытовые'),
    )

    description = models.TextField(verbose_name="Описание")
    category = models.CharField(
        max_length=50,
        choices=CATEGORIES,
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Специальное требование"
        verbose_name_plural = "Специальные требования"
        ordering = ['category', 'description']

    def __str__(self):
        return f"{self.category}: {self.description[:50]}..."

class PetRequirement(models.Model):
    SEVERITY_LEVELS = (
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий'),
        ('Критичный', 'Критичный'),
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        verbose_name="Питомец"
    )
    requirement = models.ForeignKey(
        SpecialRequirement,
        on_delete=models.CASCADE,
        verbose_name="Требование"
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVELS,
        verbose_name="Серьезность"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Требование для питомца"
        verbose_name_plural = "Требования для питомцев"
        unique_together = ('pet', 'requirement')
        ordering = ['pet', '-severity']

    def __str__(self):
        return f"{self.pet}: {self.requirement} ({self.severity})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('действительно', 'Действительно'),
        ('отменено', 'Отменено'),
        ('просрочено', 'Просрочено'),
        ('закрыто', 'Закрыто'),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Комната"
    )
    arrival_date = models.DateField(verbose_name="Дата заезда")
    departure_date = models.DateField(verbose_name="Дата выезда")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='действительно',
        verbose_name="Статус"
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Питомец"
    )
    human_count = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество гостей"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-arrival_date']

    def __str__(self):
        return f"Бронирование #{self.id} ({self.client.name})"

    @property
    def duration(self):
        return (self.departure_date - self.arrival_date).days

class Warehouse(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        verbose_name="Отель"
    )
    location = models.JSONField(verbose_name="Местоположение склада")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ['hotel']

    def __str__(self):
        return f"Склад отеля {self.hotel.name}"

class Product(models.Model):
    count = models.IntegerField(verbose_name="Количество")
    name = models.CharField(max_length=20, verbose_name="Название")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    creator = models.TextField(verbose_name="Производитель")
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        verbose_name="Склад"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.count} шт.)"

class Require(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )
    product_name = models.TextField(verbose_name="Название продукта")
    required_count = models.IntegerField(verbose_name="Требуемое количество")
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        verbose_name="Отель"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    request_date = models.DateField(verbose_name="Дата запроса")

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
        ordering = ['-request_date']

    def __str__(self):
        return f"Запрос #{self.id} ({self.product_name})"

# Create your models here.
