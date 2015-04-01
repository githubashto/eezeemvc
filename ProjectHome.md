Eezee MVC is an Easy Model, View, Controller (MVC) framework for Google App Engine.

## Features ##
  * Has a Controller Class that does routing, handling and rendering templates.
  * Your controllers reside in the controllers folder, views (html Django templates) in views folder, models in models folder.
  * Allows Controller to recieve GET/POST parameters as function arguments.
  * Use's S Nakajima's excellant [gdispatch router](http://github.com/snakajima/gdispatch).

See the project page, (which is also the example application) at http://eezeemvc.appspot.com/

You can download the source code from the download link above. What you download is the sample application and is also the project page site. Unpack it. Rename the folder to your required name, and edit that application name in "app.yaml" to your required name. Then Edit the sample application to suit your requirements.

Explanation of how it all works is given below. The sample application handles three pages, index page, about page, and contacts page.

First let us look at **main.py** in the root folder.
```
from eezee_sys.controller import Controller

from controllers import maincontroller
from controllers import contactcontroller

if __name__ == '__main__':
    Controller.run()
```

  1. First we import the "Controller" class (namespace) from eezee\_sys.controller. This controller class extends "webapp.RequestHandler", and adds some routing, handling and rendering functions to it, as we will see below.
  1. Then we import the maincontroller and contactcontroller from the controllers folder. The controllers in the controllers folder are the ones you have to write.
  1. We call the static "run()" method of the Controller class, and away we go.

Now let us look at **maincontroller.py** in the controllers folder.
```
from eezee_sys.controller import Controller

Controller.route(lambda:('/', IndexController))
class IndexController(Controller):
    def get(self):
        self.doRender('index.html', {})

Controller.route(lambda:('/about', AboutController))
class AboutController(Controller):
    def get(self):
        self.doRender('about.html', {})
```

  1. First we import the "Controller" class (namespace) from eezee\_sys.controller.
  1. Then we call the static "route()" method of the Controller class with the given parameters. (If you don't know what a lambda function is, don't worry, thats for advanced python programmers, just do the routing as shown). Here we route the "/" request to the IndexController.
  1. Then we define the class IndexController. As you can see it extends the Controller class, which in turn extends the webapp.RequestHandler.
  1. Next the get() method of the IndexController calls the "doRender()" instance method of the Controller class. This method takes two parameter. Path to an "index.html" file. This file must reside in the "views" folder and is actually a Django template. See the source's in views folder. It also extends the "base.html" Django template. All pages in this project extends base.html. The second parameter is a dictionary which contains the the template values to be passed to the Template. In this case there are no values, an empty dict is passed.
  1. The last block of code works pretty much the same way as above, for the "/about" request, in which we define a AboutController.

Here is the code for **contactcontroller.py**. I could have included this code in maincontroller.py. I have split it here as an example on how to split large controllers.
```
from eezee_sys.controller import Controller
from models.message import Message

Controller.route(lambda:('/contact', ContactController))
class ContactController(Controller):
    def get(self):
        self.doRender('contact.html', {})

    @Controller.kwargs
    def post(self, name, email, message):
        message = Message(name=name, email=email, message=message)
        message.put()
        self.redirect("/")
```

  1. First we import the "Controller" class (namespace) from eezee\_sys.controller.
  1. Next we import the "Message" class (namespace) from models.message.(See message.py in models folder).
  1. The get() method is called when the user requests "/contact" and we render contact.html, which has the contact form.
  1. The "@Controller.kwargs" line, takes the posted contact form fields, and converts them to arguments with the same "name" in the post() method.
  1. We then create a message object, supplying it with the posted values to initialize, and we save the message entity by calling its put() method. And then we redirect back to the index page.