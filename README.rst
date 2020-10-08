BottleCBV (Bottle Class Based View)
===================================

.. module:: bottleCBV

`bottleCBV` is an class based view extension for bottle framework, that will automatically generate 
routes based on methods in the views defined (Inspired by ```Flask-Classy```).

Installation
------------

Install the extension with::

    $ pip install bottleCBV

How it works
------------

Let's see how to use it whilst building something with it. 


Special Methods:
****************

HTTP methods below are treated as special methods, there are not registered based on the method name but HTTP method


``["get", "put", "post", "delete", "index", "options"] ``


Example:
********
For the very simple example, registering the all the routes in the class can be used as follow,
::

  from bottle import Bottle, run
  from bottleCBV import BottleView

  app = Bottle()
  
  class ExampleView(BottleView):

      def index(self):
          return "Index Examples"
  
      def get(self, item_key):
          return "Get Example %s" % item_key
          
      def post(self):
          return "Post Example"
          
      def put(self, item_key):
          return "Put Example %s" % item_key

      # automatically create routes for any method which is not special methods
      # also its smart enough to generate route based on number of arguments method takes
      def some_method(self, arg1, arg2)
          return "Get Some Method with %s and %s" % (arg1, arg2)

  ExampleView.register(app)
  # Run the app
  app.run(port=8080)
  
    
When you register the app it will basically register following endpoints to the app

::
  
  Method: GET 
  Endpoint: `/example/` 
  
  Method: GET 
  Endpoint: `/example/<item_key>/`
  
  Method: POST 
  Endpoint: `/example/`
  
  Method: PUT 
  Endpoint: `/example/<item_key>/`
  
  Method:  
  Endpoint: `/example/some-method/<arg1>/<arg2>/`
  

Access them as below:

::

  curl -XGET "http://localhost:8080/example/"
  OUTPUT: `Index Examples`
  
  `curl -XGET "http://localhost:8080/example/1/"`
  OUTPUT: `Get Example 1`
  
  `curl -XPOST "http://localhost:8080/example/"`
  OUTPUT: `Post Example`
      
  `curl -XPUT "http://localhost:8080/example/1/"`
  OUTPUT: `Put Example 1`

  `curl -XGET "http://localhost:8080/example/some-method/1/2/"`
  OUTPUT: `Get Some Method with 1 and 2`


Adding Custom Route:
********************
Custom Rule can add by using ```route``` decorator e.g,

::
  
  from bottleCBV import BottleView, route
  
  class ExampleView(BottleView):
      ...
      ...
      @route("/my-custom-route/", method=["GET", "POST"])
      def somemethod(self):
          return "My Custom Route"
      
      ...
      ...

So, now the route/rule registered for the method above will be,

::

  Method: GET 
  Endpoint: `/my-custom-route/` 
  
  Method: POST 
  Endpoint: `/my-custom-route/`


**Note**: ```you can obiviously add multiple routes to one method by adding additional route decorators to it with the new route/rule```


Adding decorators:
******************
To add decorator to any method you can simply use traditional way as follow,

::

  class ExampleView(BottleView):
      ...
      ...
      @mydecorator
      def somemethod(self):
          ...
      
      ...

To add decorator to all the methods in the class, simple add an attribute to the class definition with a list of decorators, 
and that will be applied to all the methods in the class

::

  class ExampleView(BottleView):
      decorators = [mydecorator1, mydecorator2,  .... ]
      
      def get(self, item_key):
          ...
          
      @route("/my-custom-route/", method=["GET", "POST"])
      def somemethod(self):
          ...
      
      ...
        
        
is same as:
 
::

    class ExampleView(BottleView):
    
        @mydecorator1
        @mydecorator2
        def get(self, item_key):
            ...
            
        @route("/my-custom-route/", method=["GET", "POST"])
        @mydecorator1
        @mydecorator2
        def somemethod(self):
            ...
        ...
        ...

Adding Route Base Prefix:
*************************
So if you want to add base prefix to your route, it is as simple as adding a variable in you View as below,
::
    class ExampleView(BottleView):
        base_route = "/my"
        ...
        ...

So, now all the routes in ExampleView will be registered as follow
::
    
    Method: GET 
    Endpoint: `/my/example/`
    
    Method: GET 
    Endpoint: `/my/example/<item_key>/`
    
    Method: POST 
    Endpoint: `/my/example/`
    
    Method: PUT 
    Endpoint: `/my/example/<item_key>/`
    
    
Adding Route Prefix:
********************
So if you want to add base prefix to your route, it is as simple as adding a variable in you View as below,

::

    class ExampleView(BottleView):
        route_prefix = "/custom-route"
        ...
        ...

So, now all the routes in ExampleView will be registered as follow

::
    
    Method: GET 
    Endpoint: `/custom-route/`
    
    Method: GET 
    Endpoint: `/custom-route/<item_key>/`
    ...
    ...

    
    Note: you can add both base_route and route_prefix, 
    that will generate combination of both e.g, ``/route_base/route_prefix/``
    
