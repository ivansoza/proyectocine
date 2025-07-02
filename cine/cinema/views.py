# cinema/views.py
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Showtime, SnackItem

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Cartelera: próximas 30 funciones ordenadas por hora
        ctx["showtimes"] = (
            Showtime.objects
            .select_related("movie", "auditorium", "auditorium__cinema")
            .filter(
                movie__is_active=True,
                auditorium__cinema__is_active=True,
            )
            .order_by("start_time")[:30]
        )
        # Snacks destacados: los 6 primeros disponibles (puedes cambiar el criterio)
        ctx["snacks"] = (
            SnackItem.objects
            .select_related("category")
            .filter(is_available=True)
            .order_by("-updated")[:6]
        )
        return ctx
