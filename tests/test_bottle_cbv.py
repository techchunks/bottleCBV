from bottle import Bottle
from .dummy_class import BasicView, IndexView, RouteBaseView

from nose.tools import *

app = Bottle()
BasicView.register(app)
IndexView.register(app)
# RouteBaseView.register(app)

# client = app.test_client()


def test_index_url():
    url = app.get_url("IndexView:index")
    eq_("/", url)


def test_basic_index_url():
    url = app.get_url("BasicView:index")
    eq_("/basic/", url)


def test_custom_endpoint_url():
    url = app.get_url("basic_endpoint")
    eq_("/basic/endpoint/", url)

#
# def test_custom_route_base():
#     with app.test_request_context():
#         url = url_for('RouteBaseView:index')
#         eq_("/base-routed/", url)
#
# def test_variable_route_popped_base():
#     with app.test_request_context():
#         url = url_for('VarBaseView:index', route='bar')
#         eq_('/var-base-route/bar/', url)
#
# def test_variable_route_base():
#     with app.test_request_context():
#         url = url_for('VarBaseView:with_base_arg', route='bar')
#         eq_('/var-base-route/bar/with_base_arg/', url)
#
#
# def test_variable_route_base_with_local_route_var():
#     client = app.test_client()
#     resp = client.get('/var-base-route/bar/local/baz')
#     eq_(resp.data, b"bar baz")
#
