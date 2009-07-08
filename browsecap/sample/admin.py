from django.contrib import admin
from browsecap.sample.models import Spam, Type

admin.site.register([Spam, Type])

