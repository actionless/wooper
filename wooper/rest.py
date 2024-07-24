"""
.. module:: rest
   :synopsis: REST functions

REST functions are receiving behave `context
<https://behave.readthedocs.io/en/stable/context_attributes.html>`_
object as first argument.
These helpers make testing API response bodies and headers easy with minimal
time and effort.

Context Variables
-----------------

The following context variables are used:

.. rubric:: To be set by user:

.. attribute:: context.server_url

    :type: str

    server base url

.. attribute:: context.enable_ssl_verification

    :type: bool = False

.. attribute:: context.print_url

    :type: bool

.. attribute:: context.print_payload

    :type: bool

.. attribute:: context.print_headers

    :type: bool


.. rubric:: Will be set by lib:

.. attribute:: context.response

    request `response
    <https://requests.readthedocs.io/en/latest/api/#requests.Response>`_

.. attribute:: context.session

    request `session
    <https://requests.readthedocs.io/en/latest/api/#requests.Session>`_

.. moduleauthor:: Yauhen Kirylau <actionless.loveless@gmail.com>

Functions
---------
"""


from pprint import pprint
import json
import os

from requests import Session

from .general import parse_json_response, apply_path


def get_url(context, uri):
    return context.server_url + uri


def request(context, method, uri, data=None, *args,
            add_server=True, **kwargs):

    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data)

    if not context.session:
        context.session = Session()

    if add_server:
        url = get_url(context, uri)
    else:
        url = uri

    if 'headers' in kwargs:
        headers = kwargs.pop('headers')
    else:
        headers = {}

    if context.print_url:
        print('{method} {url}'.format(method=method, url=url))
    if context.print_payload and 'data' in kwargs:
        print(kwargs['data'])

    if context.print_headers:
        pprint(headers)

    context.response = context.session.request(
        method,
        url,
        *args,
        data=data,
        headers=headers,
        verify=context.template_variables.get(
            'enable_ssl_verification', False
        ),
        **kwargs
    )


def GET(context, uri, *args, **kwargs):
    """
    make a GET request to some URI

    :param str uri: URI

    rest of args is the same as in `requests.get()
    <https://requests.readthedocs.io/en/latest/api/#requests.get>`_
    """
    request(context, 'GET', uri, *args, **kwargs)


def POST(context, uri, *args, **kwargs):
    """
    make a POST request to some URI

    :param str uri: URI
    :param data: request payload
    :type data: str, list, dict

    rest of args is the same as in `requests.post()
    <https://requests.readthedocs.io/en/latest/api/#requests.post>`_
    """
    request(context, 'POST', uri, *args, **kwargs)


def PATCH(context, uri, *args, **kwargs):
    """
    make a PATCH request to some URI

    :param str uri: URI
    :param data: request payload
    :type data: str, list, dict

    rest of args is the same as in `requests.patch()
    <https://requests.readthedocs.io/en/latest/api/#requests.patch>`_
    """
    request(context, 'PATCH', uri, *args, **kwargs)


def PUT(context, uri, *args, **kwargs):
    """
    make a PUT request to some URI

    :param str uri: URI
    :param data: request payload
    :type data: str, list, dict

    rest of args is the same as in `requests.put()
    <https://requests.readthedocs.io/en/latest/api/#requests.put>`_
    """
    request(context, 'PUT', uri, *args, **kwargs)


def DELETE(context, uri, *args, **kwargs):
    """
    make a DELETE request to some URI

    :param str uri: URI

    rest of args is the same as in `requests.delete()
    <https://requests.readthedocs.io/en/latest/api/#requests.delete>`_
    """
    request(context, 'DELETE', uri, *args, **kwargs)


def HEAD(context, uri, *args, **kwargs):
    """
    make a HEAD request to some URI

    :param str uri: URI

    rest of args is the same as in `requests.head()
    <https://requests.readthedocs.io/en/latest/api/#requests.head>`_
    """
    request(context, 'HEAD', uri, *args, **kwargs)


def json_response(context):
    json_dict = parse_json_response(context.response)
    return json_dict


def get_id_from_href(context, path=None):
    input_json = apply_path(json_response(context), path)
    item_id = os.path.basename(input_json['href'])
    return int(item_id)
