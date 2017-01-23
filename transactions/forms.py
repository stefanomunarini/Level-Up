from django.forms import Form, BooleanField, CharField, HiddenInput


class TransactionForm(Form):
    pid = CharField(widget=HiddenInput())
    sid = CharField(widget=HiddenInput())
    success_url = CharField(widget=HiddenInput())
    cancel_url = CharField(widget=HiddenInput())
    error_url = CharField(widget=HiddenInput())
    checksum = CharField(widget=HiddenInput())
    amount = CharField(widget=HiddenInput())
    dev = BooleanField()
