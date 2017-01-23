from django.utils.translation import ugettext_lazy as _

from screenplayreader.mixins.models import *


class BaseModel(TimeStamped, Ownable):
    class Meta:
        abstract = True

