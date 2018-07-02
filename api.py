# Syring Pump API Server

from __future__ import unicode_literals
import falcon
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems
from datetime import datetime
try:
    from stepper import Stepper

    GPIO_PA = 1
    GPIO_PA_ = 7
    GPIO_PB = 8
    GPIO_PB_ = 25

    GPIO_SWITCH_FULL = 21
    GPIO_SWITCH_EMPTY = 20

    print "Initializing Syringe Pump"
    stepper = Stepper(GPIO_PA, GPIO_PA_, GPIO_PB, GPIO_PB_, GPIO_SWITCH_FULL, GPIO_SWITCH_EMPTY)
    print "Turning off Stepper"
    stepper.off()
except Exception as ex:
    print "Error initializing Syringe Pump: " + str(ex)

class WebpageResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        with open('static/index.html', 'r') as file:
            resp.body = file.read()

class SyringPumpResource(object):

    def on_get(self, req, resp):
        print "Received {} {} request with params {}".format(req.method, req.path, req.params)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT
        if 'cmd' in req.params:
            command = req.params['cmd']
            if command == 'fill':
                stepper.step_max_cw()
                resp.body = "Syringe Pump filled"
            if command == 'empty':
                stepper.step_max_ccw()
                resp.body = "Syringe Pump emptied"
            if command == 'drop':
                stepper.step(10, Stepper.DIR_CCW)
                resp.body = "Syring Pump dispensed one drop"
        else:
            resp.status = falcon.HTTP_400
            resp.body = "ERROR: no command given"

    def on_post(self, req, resp):
        print "Received {} {} request from {}".format(req.method, req.path, req.params)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT
        question = req.stream.read()
        if question.find("time") != -1 :
            resp.body = "The time is: " + str(datetime.now()) + '\n'
        if question.find("myip") != -1 :
            resp.body += "Your IP address is: " + str(req.remote_addr) + '\n'

class SyringePumpApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(SyringePumpApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':

    print "Starting API Server"
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),
        'workers': 1,
        'timeout' : 100000
    }
    # falcon.API instances are callable WSGI apps
    app = falcon.API()

    webpage = WebpageResource()
    pump = SyringPumpResource()

    # things will handle all requests to the '/pump' URL path
    app.add_route('/', webpage)
    app.add_static_route('/static', '/Users/eashan/PycharmProjects/syringePump/static')
    app.add_route('/pump', pump)

    SyringePumpApp(app, options).run()