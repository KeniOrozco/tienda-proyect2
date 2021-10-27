from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from carrito.models import Orden

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            "ordenes": Orden.objects.filter(usuario=self.request.user, ordenada=True),
        })
        return context


class HomeView(generic.TemplateView):
    template_name = 'index.html'


class SobreNosotrosView(generic.TemplateView):
    template_name = 'nosotros.html'

