from _md5 import md5

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from games.models import Game
from levelup.settings import PAYMENT_SERVICE_SECRET_KEY, HEROKU_HOST
from transactions.models import Transaction
from users.services import send_email


class PaymentResultRedirectView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        pid = self.request.GET.get('pid')
        payment_ref = self.request.GET.get('ref')
        result = self.request.GET.get('result')
        secret_key = PAYMENT_SERVICE_SECRET_KEY
        request_checksum = self.request.GET.get('checksum')

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, payment_ref, result, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        if not request_checksum == checksum:
            raise PermissionDenied

        game = get_object_or_404(Game, slug=pid)
        save_transaction(game, request.user, result, payment_ref)

        if result != 'success':
            messages.error(request, 'There was a problem processing the payment. Please try again later!')

        return super(PaymentResultRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('game:detail', kwargs={'slug': self.request.GET.get('pid')})


@receiver(post_save, sender=Transaction, dispatch_uid="new_transaction")
def send_email_after_transaction(sender, instance, **kwargs):
    subject = _('Congratulations, you have bought {}!'.format(instance.game.name))
    send_email(subject, 'game_bought_email.html', [instance.user.user.email],
               context={'username': instance.user.user.username,
                        'game': instance.game,
                        'url': 'https://' + HEROKU_HOST})

def save_transaction(game, user, status, payment_ref=None):
    transaction = Transaction()
    transaction.game = game
    transaction.user = user.profile
    transaction.status = status
    transaction.payment_ref = payment_ref
    transaction.amount = game.price
    transaction.save()
