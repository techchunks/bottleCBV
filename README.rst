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

    ExampleView.register(app)
    # Run the app
    app.run(port=8080)
    
    
When you register the app it will basically register following endpoints to the app

Method: GET ```/example/``` 

Method: GET ```/example/<item_key>``` 

Access them as below:

    ```curl -XGET "http://localhost:8080/example/"```
    
    OUTPUT:
        ``Index Examples``
        
    
    ```curl -XGET "http://localhost:8080/example/1/"```
    
    OUTPUT:
        ``Get Example 1``
