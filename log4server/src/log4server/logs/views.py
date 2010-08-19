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
from django.core.paginator import Paginator, InvalidPage, EmptyPage

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

colors = {'FATAL' : 'Red', 
    'ERROR' : 'Magenta', 
    'TARGET' : 'LightSkyBlue'}

def paginate_logtraces(request, logtraces_list):
    paginator = Paginator(logtraces_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        logtraces = paginator.page(page)
    except (EmptyPage, InvalidPage):
        logtraces = paginator.page(paginator.num_pages)
    for logtrace in logtraces.object_list:
        logtrace.color = colors.get(logtrace.loglevel, colors['TARGET'])
    logs = Log.objects.all()
    bottom = logtraces.number - 3
    pages_iter = [bottom, logtraces.number]
    if paginator.num_pages <= 3:
        pages_iter = range(1, paginator.num_pages)
    elif logtraces.number <= 3:
        pages_iter = range(1, 6)
    else:
        pos = 1
        down = 2 
        for number in range(1, 6):
            top = logtraces.number + number
            bottom += 1
            if bottom < logtraces.number:
                pages_iter.insert(pos, logtraces.number - down)
                pos += 1
                down -= 1
            elif logtraces.has_next() and top <= paginator.num_pages:
                    pages_iter.append(top-2)
    return (logtraces, logs, pages_iter)

# contains the last searched results 
# only in the search_results page
logtraces_found = None
LAST_QUERY = None
LAST_LOGNAME = None

@allowed('GET')
def status(request):
    global logtraces_found 
    logtraces_found = None
    logtraces_list = LogTrace.objects.all().order_by('-insertion_date')
    logtraces, logs, pages_iter = paginate_logtraces(request, logtraces_list)
    return render_to_response('status.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter})

@allowed('GET')
def search(request):
    global logtraces_found
    global LAST_QUERY
    global LAST_LOGNAME
    query = request.GET.get('query')
    logname = request.GET.get('logname')
    results = 0
    if logname and query:
        LAST_QUERY = query
        LAST_LOGNAME = logname
        logtraces_list = LogTrace.objects.filter(logtrace__contains = query, 
                log__logpath = logname)
        logtraces_found = logtraces_list
    elif query:
        LAST_QUERY = query
        logtraces_list = LogTrace.objects.filter(logtrace__contains = query)
        logtraces_found = logtraces_list
    else:
        # no query was introduced in search box
        return render_to_response('base_no_search.html', {'logs' :
            Log.objects.all()})

    logtraces, logs, pages_iter = paginate_logtraces(request, logtraces_found)
    return render_to_response('search_results.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter, 
        'query' : LAST_QUERY, 'num_results' : len(logtraces_found),
        'logname' : LAST_LOGNAME})

@allowed('GET')
def showonly(request):
    global logtraces_found
    global LAST_LOGNAME
    logname = request.GET.get('logname')
    if logname:
        LAST_LOGNAME = logname
        logtraces_list = (LogTrace.objects.
                filter(log__logpath=logname).
                order_by('-insertion_date'))
        logtraces_found = logtraces_list
    logtraces, logs, pages_iter = paginate_logtraces(request, logtraces_found)
    return render_to_response('showonly.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter,
        'logname' : LAST_LOGNAME})

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


