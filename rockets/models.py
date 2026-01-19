from django.db import models


class Cosmodrome(models.Model):
    """Модель космодрома"""
    name = models.CharField('Название', max_length=200)
    country = models.CharField('Страна', max_length=100)
    location = models.CharField('Местоположение', max_length=300)
    founded_year = models.IntegerField('Год основания', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Действующий', default=True)

    class Meta:
        verbose_name = 'Космодром'
        verbose_name_plural = 'Космодромы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.country})"


class Rocket(models.Model):
    """Модель ракеты"""
    ROCKET_TYPES = [
        ('orbital', 'Орбитальная'),
        ('suborbital', 'Суборбитальная'),
        ('heavy', 'Тяжёлая'),
        ('super_heavy', 'Сверхтяжёлая'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('retired', 'Выведена из эксплуатации'),
        ('development', 'В разработке'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=200)
    country = models.CharField('Страна', max_length=100)
    rocket_type = models.CharField('Тип ракеты', max_length=20, choices=ROCKET_TYPES, default='orbital')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    first_flight_year = models.IntegerField('Год первого полёта', null=True, blank=True)
    height = models.DecimalField('Высота (м)', max_digits=6, decimal_places=2, null=True, blank=True)
    diameter = models.DecimalField('Диаметр (м)', max_digits=5, decimal_places=2, null=True, blank=True)
    mass = models.DecimalField('Масса (т)', max_digits=10, decimal_places=2, null=True, blank=True)
    payload_to_leo = models.DecimalField('Полезная нагрузка на НОО (кг)', max_digits=10, decimal_places=2, null=True, blank=True)
    stages = models.IntegerField('Количество ступеней', default=2)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Ракета'
        verbose_name_plural = 'Ракеты'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.manufacturer})"


class Launch(models.Model):
    """Модель запуска/миссии"""
    STATUS_CHOICES = [
        ('success', 'Успешный'),
        ('failure', 'Неудачный'),
        ('partial', 'Частично успешный'),
        ('planned', 'Запланирован'),
    ]
    
    mission_name = models.CharField('Название миссии', max_length=300)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE, related_name='launches', verbose_name='Ракета')
    cosmodrome = models.ForeignKey(Cosmodrome, on_delete=models.CASCADE, related_name='launches', verbose_name='Космодром')
    launch_date = models.DateTimeField('Дата и время запуска')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='planned')
    payload = models.CharField('Полезная нагрузка', max_length=500, blank=True)
    orbit = models.CharField('Орбита', max_length=100, blank=True)
    description = models.TextField('Описание миссии', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запуск'
        verbose_name_plural = 'Запуски'
        ordering = ['-launch_date']

    def __str__(self):
        return f"{self.mission_name} - {self.rocket.name} ({self.launch_date.strftime('%d.%m.%Y')})"
