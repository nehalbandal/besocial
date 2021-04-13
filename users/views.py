from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class Registration(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Registration'
        return context


class UpdateUserProfile(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/update_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Update Profile'
        return context


class UserProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'User Profile'
        return context