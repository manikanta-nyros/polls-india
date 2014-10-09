from django.forms.util import flatatt
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class StarsRadioInput(RadioChoiceInput):

    def __init__(self, *args, **kwargs):
        msg = "RadioInput has been deprecated. Use RadioChoiceInput instead."
        warnings.warn(msg, PendingDeprecationWarning, stacklevel=2)
        super(StarsRadioInput, self).__init__(*args, **kwargs)


class StarsRadioChoiceInput(ChoiceInput):
    input_type = 'radio'

    def __init__(self, *args, **kwargs):
        super(StarsRadioChoiceInput, self).__init__(*args, **kwargs)
        self.value = force_text(self.value)

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
            final_attrs = dict(
                self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


class StarsRadioFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = StarsRadioChoiceInput

    def render(self):
        return mark_safe(u'\n%s\n' % u'\n'.join([u'%s' % force_unicode(w) for w in self]))
