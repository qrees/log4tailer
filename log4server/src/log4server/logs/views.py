# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import (HttpResponse, 
        HttpResponseNotFound,
        HttpResponseBadRequest)
from models import Log, LogTrace
from django.utils import simplejson as json

def allowed(verb):
    def required(func):
        def wrapper(request, *args, **kwargs):
            if request.method != verb:
                return HttpResponseNotFound()
            return func(request, *args, **kwargs)
        return wrapper
    return required

def data_required(func):
    def wrapper(request, *args, **kwargs):
        data = json.loads(request.raw_post_data)
        request.data = data
        if not data:
            return HttpResponseBadRequest("data not found in request")
        return func(request, *args, **kwargs)
    return wrapper

def from_json(model, data):
    vals = {}
    # model must have an static method 
    # json mapper that returns a dict with callables 
    # or None
    to_model = model.json_mapper()
    for key, value in data.iteritems():
        if key in to_model and callable(to_model[key]):
            vals[key] = to_model[key](**value)
        else:
            vals[key] = value
    return vals

@allowed('POST')
@data_required
def alert(request):
    data = request.data
    params = from_json(LogTrace, data)
    incoming_log = params.get('log', None)
    incoming_logtrace = params.get('logtrace', None)
    if not (incoming_log and incoming_logtrace):
        return HttpResponseBadRequest("Not enough information provided")
    get_object_or_404(Log, logpath = incoming_log.logpath, logserver =
            incoming_log.logserver)
    logtrace = LogTrace(**params)
    logtrace.save()
    return HttpResponse(content='', status=201)

@allowed('GET')
def status(request):
    logs = Log.objects.all()
    return HttpResponse(content = logs, status = 200)
    
@allowed('POST')
@data_required
def register(request):
    data = request.data
    logpath = data.get('logpath', None)
    logserver = data.get('logserver', None)
    if not (logpath and logserver):
        return HttpResponseBadRequest("Not enough information provided")
    num_logs = Log.objects.filter(logpath = logpath, logserver = logserver).count()
    if not num_logs:
        log = Log(**data)
        log.save()
    return HttpResponse(status = 201)
    

