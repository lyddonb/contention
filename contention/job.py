import logging
import uuid
from datetime import datetime

from google.appengine.ext import ndb

from furious import context
from furious.async import Async


class State(ndb.Model):

    start_time = ndb.DateTimeProperty(auto_now_add=True)
    modified_time = ndb.DateTimeProperty(auto_now=True)


class RunState(State):
    counter = ndb.IntegerProperty(default=0)
    count_map = ndb.JsonProperty()

    @property
    def count_map_count(self):
        return len(self.count_map)


class CompleteState(State):
    complete = ndb.BooleanProperty()
    number_of_items = ndb.IntegerProperty()


def start(number_of_items):
    logging.info("******** Starting the process. ******** ")
    job_id = uuid.uuid4().hex
    logging.info("******* JOB ID: {}.".format(job_id))

    start_time = _get_current_datetime_as_string()

    rs = RunState(id=job_id)
    rs.count_map = {}

    cs = CompleteState(id=job_id)
    cs.number_of_items = number_of_items
    cs.complete = False

    ndb.put_multi([rs, cs])

    with context.new() as ctx:
        ctx.set_event_handler('complete', Async(
            completion_handler, args=[job_id, start_time]))

        for i in xrange(number_of_items):
            logging.info("###### JOB ITEM: {}.".format(i))
            ctx.add(target=run_process,
                    args=[job_id, i, _get_current_datetime_as_string()])

    logging.info("###### JOBS STARTED")

    return job_id


def run_process(job_id, count, current_date_time):
    logging.info("###### Processing: {}, {}".format(job_id, count))

    @ndb.transactional()
    def _txn():
        rs = RunState.get_by_id(job_id)
        rs.counter += 1
        if not rs.count_map:
            rs.count_map = {}
        rs.count_map[count] = _get_current_datetime_as_string()
        logging.info("@@@@@@@@ Updating counter: {}".format(rs.counter))
        logging.info("@@@@@@@@ Updating count map: {}".format(rs.count_map))
        rs.put()

    _txn()


def completion_handler(job_id, start_time):

    @ndb.transactional()
    def _txn():
        logging.info("&&&&&&&&& Completing Job: {}".format(job_id))
        cs = CompleteState.get_by_id(job_id)
        cs.complete = True
        cs.put()

    _txn()

    logging.info("******** Process complete. ******** ")


def _get_current_datetime_as_string():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
