import unittest

from bottle import Bottle
from nose.tools import *
from webtest import TestApp

from .dummy_class import BasicView, RouteBaseView, RoutePrefixView
from .dummy_class import DecoratorView, SingleDecoratorView


app = Bottle()
BasicView.register(app)
RouteBaseView.register(app)
RoutePrefixView.register(app)
DecoratorView.register(app)
SingleDecoratorView.register(app)

test_app = TestApp(app)

class TestBasicView(unittest.TestCase):
    def test_basic_index_url(self):
        response = test_app.get("/basic/")
        eq_("Index", response.body)


    def test_basic_get_url(self):
        response = test_app.get("/basic/1234/")
        eq_("Get:1234", response.body)


    def test_basic_post_url(self):
        response = test_app.post("/basic/")
        eq_("Post", response.body)


    def test_mymethod_get_url(self):
        response = test_app.get("/basic/mymethod/")
        eq_("My Method", response.body)


    def test_mymethod_with_params_get_url(self):
        response = test_app.get("/basic/mymethod-args/arg1/arg2/")
        eq_("My Method arg1 arg2", response.body)


    def test_mymethod_custom_route_get(self):
        response = test_app.get("/endpoint/")
        eq_("Custom Route", response.body)


    def test_mymethod_custom_route_post(self):
        response = test_app.post("/endpoint/")
        eq_("Custom Route POST", response.body)
        response = test_app.put("/endpoint/")
        eq_("Custom Route PUT", response.body)


    def test_multi_route_method(self):
        response = test_app.get("/route1/")
        eq_("Multi Routed Method", response.body)
        response = test_app.get("/route2/")
        eq_("Multi Routed Method", response.body)


class TestRouteBase(unittest.TestCase):

    def test_route_base(self):
        response = test_app.get("/my/routebase/")
        eq_("index-route-base", response.body)


class TestRoutePrefix(unittest.TestCase):

    def test_route_base(self):
        response = test_app.get("/")
        eq_("index-route-prefix", response.body)


class TestDecorators(unittest.TestCase):

    def test_route_base(self):
        response = test_app.get("/decorator/")
        eq_("decorator:index", response.body)

    def test_route_base_post(self):
        response = test_app.post("/decorator/")
        eq_("decorator:post", response.body)

    def test_route_base_get(self):
        response = test_app.get("/decorator/123/")
        eq_("decorator:get:123", response.body)

    def test_route_base_myfunc(self):
        response = test_app.get("/decorator/myfunc/123/")
        eq_("decorator:get:myfunc:123", response.body)

    def test_route_base_my_custom_route(self):
        response = test_app.get("/my-custom-route/")
        eq_("decorator:get:my-custom-route", response.body)


class TestSingleDecorator(unittest.TestCase):

    def test_route_base(self):
        response = test_app.get("/singledecorator/")
        eq_("index", response.body)

    def test_route_base_post(self):
        response = test_app.post("/singledecorator/")
        eq_("decorator:post", response.body)

    def test_route_base_get(self):
        response = test_app.get("/singledecorator/123/")
        eq_("get:123", response.body)
