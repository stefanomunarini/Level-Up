from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from users.models import UserProfile


class ApiToken(models.Model):
    developer = models.ForeignKey(UserProfile, related_name='api_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=36, unique=True, null=False)
    website_url = models.URLField(_('The website in where you will use this token'), null=False, blank=False)
