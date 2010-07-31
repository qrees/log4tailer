# Create your views here.
from django.http import Http404, HttpResponse
from models import Log

def alert(request):
    if not request.method == 'POST':
        raise Http404
    params = request.POST
    if not (params.get('logtrace', None) or 
            not params.get('logpath', None)):
        raise Http404
    log = Log(**params)
    log.save()
    return HttpResponse(content='', status=201)

def info(request):
    if not request.method == 'GET':
        raise Http404
    
    #TODO must do a render to response after
    #querying db
    return HttpResponse(content='', status=200)


