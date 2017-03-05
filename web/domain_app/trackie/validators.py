from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class FileSizeMaxValidator:
    message = _('The file exceeds the maximum permitted file size of %.2f MiB')
    code = 'limit_value'

    def __init__(self, limit_value, message=None):
        self.limit_value = limit_value
        if message:
            self.message = message

    def __call__(self, value):
        if self.limit_value < value.size:
            raise ValidationError(
                self.message % (float(self.limit_value)/1024/1024),
                code=self.code
            )
