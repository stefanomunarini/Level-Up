from _md5 import md5

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from games.models import Game
from levelup.settings import PAYMENT_SERVICE_SECRET_KEY
from transactions.models import Transaction


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
        transaction = Transaction()
        transaction.game = game
        transaction.user = self.request.user.profile
        transaction.status = result
        transaction.payment_ref = payment_ref
        transaction.amount = game.price
        transaction.save()

        return super(PaymentResultRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('game:detail', kwargs={'slug': self.request.GET.get('pid')})
