from django.middleware import MiddlewareBase
from django.conf import settings

STAT_COLLECTOR_SCRIPT = """
<script src="https://cdn.statcollector.com/collector.js"></script>
<script>
    StatCollector.init('%s');
</script>
"""

class StatCollectorMiddleware(MiddlewareBase):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        if (
            hasattr(response, 'content') and 
            '</body>' in response.content.decode('utf-8') and
            getattr(settings, 'STAT_COLLECTOR_ENABLED', False)
        ):
            content = response.content.decode('utf-8')
            script = STAT_COLLECTOR_SCRIPT % settings.STAT_COLLECTOR_API_KEY
            content = content.replace('</body>', f'{script}</body>')
            response.content = content.encode('utf-8')
            
        return response
