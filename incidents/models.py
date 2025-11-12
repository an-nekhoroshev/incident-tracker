from django.db import models

class Incident(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'Новый'),
        ('IN_PROGRESS', 'В работе'),
        ('RESOLVED', 'Решён'),
        ('CLOSED', 'Закрыт')
    )
    
    SOURCE_CHOICES = (
        ('OPERATOR', 'Оператор'),
        ('MONITORING', 'Мониторинг'),
        ('PARTNER', 'Партнёр')
    )

    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
