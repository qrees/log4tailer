# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseNotFound
from models import Log

try:
    import json
except:
    import simplejson as json


def allowed(verb):
    def required(func):
        def wrapper(request, *args, **kwargs):
            if request.method != verb:
                return HttpResponseNotFound()
            return func(request, *args, **kwargs)
        return wrapper
    return required

def from_json(model, request):
    data_dict = json.loads(request.raw_post_data)
    vals = {}
    # model must have an static method 
    # json mapper that returns a dict with callables 
    # or None
    to_model = model.json_mapper()
    for key, value in data_dict.iteritems():
        if key in to_model and callable(to_model[key]):
            vals[key] = to_model[key](**value)
        else:
            vals[key] = value
    return vals

@allowed('POST')
def alert(request):
    params = request.POST
    if not (params.get('logtrace', None) or 
            not params.get('logpath', None)):
        return HttpResponseNotFound()
    log = Log(**params)
    log.save()
    return HttpResponse(content='', status=201)

@allowed('GET')
def info(request):
    logs = Log.objects.all()
    pass
    


