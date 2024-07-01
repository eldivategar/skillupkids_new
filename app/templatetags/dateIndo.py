from django import template
from django.utils.dateformat import DateFormat
from django.utils.translation import gettext as _
import datetime

register = template.Library()

@register.filter
def format_timestamp(value):
    if isinstance(value, datetime.datetime):
        months = {
            1: _('Januari'), 2: _('Februari'), 3: _('Maret'), 4: _('April'),
            5: _('Mei'), 6: _('Juni'), 7: _('Juli'), 8: _('Agustus'),
            9: _('September'), 10: _('Oktober'), 11: _('November'), 12: _('Desember')
        }
        day = value.day
        month = months[value.month]
        year = value.year
        return f"{day} {month} {year}"
    return value
