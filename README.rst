BottleCBV (Bottle Class Based View)
=============

.. module:: bottleCBV

`bottleCBV` is an class based view extension for bottle framework, that will automatically generate 
routes based on methods in the views defined (Inspired by `Flask-Classy <http://github.com/apiguy/flask-classy>`_).

Installation
------------

Install the extension with::

    $ pip install bottleCBV

How it works
------------

Let's see how to use it whilst building something with it. 

For the very simple example, registering the all the routes in the class can be used as follow,

::

    from bottle import Bottle, run
    from bottleCBV import BottleView

::

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
            

    ExampleView.register(app)
    # Run the app
    app.run(port=8080)
    
    
When you register the app it will basically register following endpoints to the app

Method: GET ```/example/``` 

Method: GET ```/example/<item_key>/``` 

Method: POST ```/example/``` 

Method: PUT ```/example/<item_key>/``` 

Access them as below:

    ```curl -XGET "http://localhost:8080/example/"```
    
    OUTPUT:
        ``Index Examples``
        
    
    ```curl -XGET "http://localhost:8080/example/1/"```
    
    OUTPUT:
        ``Get Example 1``


    ```curl -XPOST "http://localhost:8080/example/"```
    
    OUTPUT:
        ``Post Example``
        
        
    ```curl -XPUT "http://localhost:8080/example/1/"```
    
    OUTPUT:
        ``Put Example 1``


Special Methods:
****************

HTTP methods below are treated as special methods, there are not registered based on the method name but HTTP method


```["get", "put", "post", "delete", "index", "options"] ```

as you can see in example above `get` request goes to ```def get```, and similarly `post` request goes to ```def post``` and so on.


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
    
    Method: GET ```/my/example/``` 
    
    Method: GET ```/my/example/<item_key>/``` 
    
    Method: POST ```/my/example/``` 
    
    Method: PUT ```/my/example/<item_key>/``` 
    

Registering Custom Methods:
***************************
Registering custom method is very simple, just need to add the method to class 
