# Create your views here.
from django.http import Http404, HttpResponse
from models import Log

def alert(request):
    if not request.method == 'POST':
        return Http404
    params = request.POST
    log = Log(logtrace = params.get('logtrace', None), 
            logpath = params.get('logpath', None))
    log.save()
    return HttpResponse(content='', status=201)


