from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from accounts.models import Psychologist
from accounts.forms.profile import ProfileEditForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = self.request.user.patients.all()
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Psychologist
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user