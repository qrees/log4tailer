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
from django.core.exceptions import ObjectDoesNotExist


###### Convenience decorators 

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


###### Request handlers

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


class LogQueries(object):
    """Just a wrapper to mantain 
    a record of what was last log to 
    be queried. Avoids having global declarations
    in several handlers"""
    def __init__(self):
        self.logtraces_found = None
        self.last_query = None
        self.last_logname = None

    def reset(self):
        """Convenience method. 
        """ 
        self.logtraces_found = None
        self.last_logname = None
        self.last_query = None
        

# contains the last searched results 
# only in the search_results page
logqueries = LogQueries()

@allowed('GET')
def status(request):
    logqueries.reset()
    logtraces_list = LogTrace.objects.all().order_by('-insertion_date')
    logtraces, logs, pages_iter = paginate_logtraces(request, logtraces_list)
    return render_to_response('status.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter})

@allowed('GET')
def search(request):
    query = request.GET.get('query')
    logname = request.GET.get('logname')
    results = 0
    if logname and query:
        logqueries.last_query = query
        logqueries.last_logname = logname
        logtraces_list = LogTrace.objects.filter(logtrace__contains = query, 
                log__logpath = logname)
        logqueries.logtraces_found = logtraces_list
    # no logname, just query
    elif query:
        logqueries.last_query = query
        logtraces_list = LogTrace.objects.filter(logtrace__contains = query)
        logqueries.logtraces_found = logtraces_list
    # no logname, no query and no query introduced before = empty
    elif not logqueries.last_query:
        return render_to_response('base_no_search.html', {'logs' :
            Log.objects.all()})

    logtraces, logs, pages_iter = paginate_logtraces(request, 
            logqueries.logtraces_found)
    return render_to_response('search_results.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter, 
        'query' : logqueries.last_query, 
        'num_results' : len(logqueries.logtraces_found),
        'logname' : logqueries.last_logname})

@allowed('GET')
def showonly(request):
    logqueries.last_query = None
    logname = request.GET.get('logname')
    if logname:
        logqueries.last_logname = logname
        logtraces_list = (LogTrace.objects.
                filter(log__logpath=logname).
                order_by('-insertion_date'))
        logqueries.logtraces_found = logtraces_list
    logtraces, logs, pages_iter = paginate_logtraces(request, 
            logqueries.logtraces_found)
    return render_to_response('showonly.html', {'logs' : logs, 
        'logtraces' : logtraces, 'pages_iter' : pages_iter,
        'logname' : logqueries.last_logname})

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

@allowed('POST')
@data_required
def unregister(request):
    data = request.data
    log_id = data.get('id', None)
    if not log_id:
        return HttpResponseNotFound("Missing log_id for unregistering")
    try:
        log = Log.objects.get(pk = log_id)
    except ObjectDoesNotExist, err:
        return HttpResponseNotFound("Log already unregistered")
    log.delete()
    return HttpResponse(status = 200)

