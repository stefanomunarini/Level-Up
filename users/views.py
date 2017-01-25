import uuid, json
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from games.models import Game
from users.forms import (
    SignupPlayerForm, SignupDeveloperForm,
    UserUpdateModelForm, UserProfileUpdateModelFormset,
    ApiKeyForm)
from users.models import UserProfile
from transactions.models import Transaction


# User Signup

class SignupUserGroupSelectionView(TemplateView):
    template_name = 'signup_user_group_selection.html'


class AbstractSignupView(FormView):
    """
    This acts as a generic SignupView that is used by SignupPlayerView and SignupDeveloperView
    """
    success_url = reverse_lazy('profile:user-profile')

    def get(self, request, *args, **kwargs):
        # Don’t allow signups if the user is already logged in
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(AbstractSignupView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        new_user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, new_user)
        return super(AbstractSignupView, self).form_valid(self)


class SignupPlayerView(AbstractSignupView):
    form_class = SignupPlayerForm
    template_name = 'signup_player.html'


class SignupDeveloperView(AbstractSignupView):
    form_class = SignupDeveloperForm
    template_name = 'signup_developer.html'


class UserProfileDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'user_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)

        if self.request.user.profile.is_developer:
            # the developer’s games
            games = Game.objects.filter(dev=self.request.user.profile)
            context['games'] = games

            # combined sales of the games
            transactions = Transaction.objects\
                .filter(game__in=games, status=Transaction.SUCCESS_STATUS)\
                .order_by('datetime')\
                .values('datetime','amount')
            sales = []
            profits = []
            for transaction in transactions:
                date_iso = transaction['datetime'].date().isoformat()
                # if no records, add the first record
                if not sales:
                    sales += [{'x': date_iso, 'y': 1}, ]
                    profits += [{'x': date_iso, 'y': transaction['amount']}, ]
                else:
                    # set value of days without transactions to zero
                    while date_iso != sales[-1]['x']:
                        # take
                        last_date_iso = datetime.strptime(sales[-1]['x'], '%Y-%m-%d')
                        next_date_iso = (last_date_iso + timedelta(1)).date().isoformat()
                        sales += [{'x': next_date_iso, 'y': 0},]
                        profits += [{'x': next_date_iso, 'y': 0},]
                    sales[-1]['y'] += 1
                    profits[-1]['y'] += transaction['amount']

            context['sales'] = json.dumps(sales)
            context['profits'] = json.dumps(profits)

            context['sales_and_profits_chart'] = {
                'y_left': {
                    'type': 'line',
                    'title': _('Sales'),
                    'color': '#008CBA',
                    'data': json.dumps(sales),
                    'format': '#',
                },
                'y_right': {
                    'type': 'line',
                    'title': _('Profits'),
                    'color': '#43AC6A',
                    'data': json.dumps(profits),
                    'format': '#',
                },
                'x_interval_type': 'day',
                'x_format': 'DD MMM YY',
            }

        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateModelForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'user_profile_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelFormset(
            queryset=UserProfile.objects.filter(user=self.get_object())
        )
        return self.render_to_response(self.get_context_data(user_form=user_form, user_profile_form=user_profile_form))

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelFormset(
            request.POST,
            request.FILES
        )
        if user_form.is_valid():
            user_form.save(commit=False)
            if user_profile_form.is_valid():
                user_profile_form.save(commit=False)
                """
                There is always one and only one formset (one user_profile for every user)
                hence we only and always save the first formset
                """
                user_profile_form[0].instance.user = self.get_object()
                user_profile_form[0].save()
                user_form.save()
                return super(UserProfileUpdateView, self).form_valid(form=user_form)
        return render(request, self.template_name, {'user_form': user_form, 'user_profile_form': user_profile_form})


class NewApiKeyView(FormView):
    form_class = ApiKeyForm
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'new_api_key.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.developer = self.request.user.profile
        form.instance.developer_id = self.request.user.profile.id
        form.instance.token = str(uuid.uuid4())
        form.save()
        return super(NewApiKeyView, self).form_valid(self)
