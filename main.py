import webapp2

from furious.handlers.webapp import AsyncJobHandler
from contention import web

webapp2_config = {
    'webapp2_extras.jinja2': {
        'globals': {
            'uri_for': webapp2.uri_for
        },
    }
}

furious_app = webapp2.WSGIApplication([
    ('/_queue/async.*', AsyncJobHandler),
])


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=web.IndexHandler, name='home'),
    webapp2.Route(r'/jobs', handler=web.JobsHandler, name='jobs'),
    webapp2.Route(r'/jobs/<job_id:(.*)>', handler=web.JobStateHandler,
                  name='job_detail'),
], debug=True, config=webapp2_config)
