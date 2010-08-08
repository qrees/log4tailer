# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2010 Jordi Carrillo Bosch

# This file is part of Log4Tailer Project.
#
# Log4Tailer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Log4Tailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Log4Tailer.  If not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import get_object_or_404, render_to_response
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
    get_object_or_404(Log, id = incoming_log.id)
    logtrace = LogTrace(**params)
    logtrace.save()
    return HttpResponse(content='', status=201)

colors = {'FATAL' : 'Red', 'ERROR' : 'Magenta', 'TARGET' : 'LightSkyBlue'}

@allowed('GET')
def status(request):
    logtraces = LogTrace.objects.all().order_by('-insertion_date')[:10]
    for logtrace in logtraces:
        logtrace.color = colors.get(logtrace.level, colors['TARGET'])
    logs = Log.objects.all()
    return render_to_response('status.html', 
            {'logs' : logs, 'logtraces' : logtraces})
    
@allowed('POST')
@data_required
def register(request):
    data = request.data
    logpath = data.get('logpath', None)
    logserver = data.get('logserver', None)
    if not (logpath and logserver):
        return HttpResponseBadRequest("Not enough information provided")
    logs = Log.objects.filter(logpath = logpath, logserver = logserver)
    if len(logs) == 0:
        log = Log(**data)
        log.save()
    else: 
        # there could be more than one (logs identified by ids, 
        # just grab first one
        log = logs[0]
    return HttpResponse(content = log.id, status = 201)
    

