#
# Copyright (c) 2009 Satoshi Nakajima
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def memoize(original_func):
    """ This decorator memorize cached data in global memory """
    cache = {}
    def decorated_func(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = original_func(*args)
            return cache[args]
    return decorated_func

@memoize
def _routing_functions():
    """ List of routing functions. Singleton. """
    return []

def route(callback_func):
    """ This simply registers a routing function, which returns a 
        (url, request_handler_class) tuple.
        Later, we call each function to generate the URL mapping.
        This defered registration mechanism allows developers to put
        dispatch.route() BEFORE the definition of the RequestHandler
        class.
    """
    _routing_functions().append(callback_func)

@memoize
def _url_mapping():
    """ The list of (url, request_handler_class) tuples. Singleton. """
    return [f() for f in _routing_functions()]
    
def run(debug=True):
    application = webapp.WSGIApplication(_url_mapping(), debug=debug)
    run_wsgi_app(application)

def get_application(debug=True):
    """ For unit testing """
    return webapp.WSGIApplication(_url_mapping(), debug=debug)

def kwargs(original_func):
    """ This decorator allows RequestHandlers to receive get/post parameters as named arguments """
    import inspect
    argspec = inspect.getargspec(original_func) 
    args = tuple(argspec[0][1:])
    def decorated_func(rh):
        kwargs = dict([(arg, rh.request.get(arg)) for arg in args])
        return original_func(rh, **kwargs)
    return decorated_func

