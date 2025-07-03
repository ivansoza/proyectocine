# cinema/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auditorium, Seat

@receiver(post_save, sender=Auditorium)
def create_seats_for_auditorium(sender, instance: Auditorium, created, **kwargs):
    """
    Al crear una nueva Auditorium, genera automáticamente todos los Seat
    según total_rows y total_cols.
    """
    if not created:
        return

    seats = [
        Seat(auditorium=instance, row=r, col=c)
        for r in range(1, instance.total_rows + 1)
        for c in range(1, instance.total_cols + 1)
    ]
    Seat.objects.bulk_create(seats)
