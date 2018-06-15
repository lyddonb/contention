import webapp2
from webapp2_extras import jinja2
from urllib import quote_plus

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from contention.job import CompleteState
from contention.job import RunState
from contention.job import start


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory)

    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class IndexHandler(BaseHandler):

    def get(self):
        self.render_response("index.html")

    def post(self):
        number_of_items = int(self.request.get("number_of_items", 1))

        job_id = start(number_of_items)

        self.redirect(webapp2.uri_for('job_detail', job_id=job_id))


class JobsHandler(BaseHandler):

    def get(self):
        curs = Cursor(urlsafe=self.request.get("cursor"))

        page_size = int(self.request.get("page_size", 10))

        q = CompleteState.query()
        q = self._modify_query(q)

        items, next_cursor, more = q.fetch_page(page_size, start_cursor=curs)

        self.render_response(
            'jobs.html', items=items, more_results=more,
            next_cursor=next_cursor.urlsafe() if next_cursor else None,
            page_size=page_size)

    def _modify_query(self, q):
        return q


class JobStateHandler(BaseHandler):

    def get(self, job_id):
        cs, rs = ndb.get_multi([ndb.Key(CompleteState, job_id),
                                ndb.Key(RunState, job_id)])

        self.render_response('job_state.html', complete_state=cs, run_state=rs)


def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.globals.update({
        'uri_for': webapp2.uri_for,
        'quote_plus': quote_plus
    })
    return j
