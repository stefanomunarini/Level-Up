from django.views.generic import DetailView
from users.models import UserProfile


class UserProfileDetailView(DetailView):
    model = UserProfile
    context_object_name = 'user_profile'
    template_name = 'user_profile_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['something'] = 'This is how you set something in the context in a Django class-based view.'
        return context
