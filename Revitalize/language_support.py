from django.db import models
from django.utils.translation import gettext_lazy as _


class LangCode(models.TextChoices):
    UNKNOWN = '?', _('Unknown')
    ENGLISH = 'EN', _('English')
    FRENCH = 'FR', _('French')


def database_to_string(entry, lang=LangCode.ENGLISH.value, default=None):
    s = entry.value if entry is not None else default
    if lang == LangCode.ENGLISH.value:
        # English is default
        pass
    elif lang == LangCode.FRENCH.value:
        # TODO
        pass
    return s