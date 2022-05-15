from django_hosts import patterns, host
from . import settings

host_patterns = patterns('',
                         host(r'', 'hacaton.urls', name='empty'),
                         host(r'app', 'app.urls', name='app'),
                         )


