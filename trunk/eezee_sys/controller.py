#
# Copyright 2010 Santosh Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import gdispatch

		
class Controller(webapp.RequestHandler):
    """ A Controller Class """
    def route(cb):
        gdispatch.route(cb)
    route = staticmethod(route)

    def run():
        gdispatch.run()
    run = staticmethod(run)

    def kwargs(original_func):
        return gdispatch.kwargs(original_func)
    kwargs = staticmethod(kwargs)
	
    def doRender(self, template_name, template_values):
        self.response.out.write(template.render('views/' + template_name, template_values))
