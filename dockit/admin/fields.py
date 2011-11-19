from django.forms import fields, widgets, ValidationError
from django.core.urlresolvers import reverse

from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils import simplejson as json

from dockit.forms.fields import HiddenJSONField

class DotPathWidget(widgets.Input):
    input_type = 'submit'
    
    def __init__(self, dotpath):
        self.dotpath = dotpath
        super(DotPathWidget, self).__init__()
    
    def render_button(self, dotpath, label=None):
        submit_attrs = self.build_attrs({}, type=self.input_type, name='_next_dotpath', value=dotpath)
        return mark_safe(u'<input%s />' % flatatt(submit_attrs))
    
    def prep_value(self, value):
        if isinstance(value, list):
            new_values = list()
            for item in value:
                if hasattr(item, 'to_primitive'):
                    item = item.to_primitive(item)
                new_values.append(item)
            value = new_values
        if hasattr(value, 'to_primitive'):
            value = value.to_primitive(value)
        if value is None:
            return ''
        elif not isinstance(value, basestring): 
            return json.dumps(value)
        return value
    
    def render(self, name, value, attrs=None):
        path_parts = list()
        if self.dotpath:
            path_parts.append(self.dotpath)
        path_parts.append(name) #TODO consider this will break if there is a prefix!
        dotpath = '.'.join(path_parts)
        json_value = self.prep_value(value)
        
        data_attrs = self.build_attrs(attrs, type='hidden', name=name, value=json_value)
        data_html = mark_safe(u'<input%s />' % flatatt(data_attrs))
        
        if isinstance(value, list):
            rows = list()
            for index, item in enumerate(value):
                item_dotpath = '%s.%s' % (dotpath, index)
                butn_html = self.render_button(item_dotpath)
                rows.append('<td>%s</td><td>%s</td>' % (escape(force_unicode(item)), butn_html))
            item_dotpath = '%s.%s' % (dotpath, index+1)
            butn_html = self.render_button(item_dotpath)
            rows.append('<td></td><td>%s</td>' % butn_html)
            return mark_safe('%s<table><tr>%s</tr></table>' % (data_html, '</tr><tr>'.join(rows)))
        else:
            butn_html = self.render_button(dotpath)
            return mark_safe(''.join((data_html, butn_html)))

class DotPathField(HiddenJSONField):
    widget = DotPathWidget
    
    def __init__(self, *args, **kwargs):
        self.dotpath = kwargs.pop('dotpath')
        if 'widget' not in kwargs:
            kwargs['widget'] = self.widget(dotpath=self.dotpath)
        super(DotPathField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if isinstance(value, basestring):
            if not value:
                return None
            return json.loads(value)
        return value

