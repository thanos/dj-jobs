#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-jobs
------------

Tests for `dj-jobs` models module.
"""

from django.test import TestCase

from djjobs import models


class TestDjjobs(TestCase):

    def setUp(self):
        pass

    def test_creating_a_job(self):
        from django.utils.text import slugify
        label = 'test_job'
        job =  models.Job.objects.create(
            label = label,
            description = 'a test job for testing slug'
        )
        assert job.slug == slugify(label), "slugify not working: %s" % `job.slug`
        assert job.run_type == job.TYPE_CRON, "run type default wrong: %s" % `job.run_type`
        assert job.enabled == False, "Should be disabled but is %s" % job.enabled

    def test_starting_a_job(self):
        label = 'test_job'
        job =  models.Job.objects.create(
            label = label,
            description = 'a test job for testing slug'
        )
        run = job.start()
        assert run.job == job, "job was not set for run %s" % run.pk
        assert run.state == run.STATUS_RUNNING, "state not switcted to running but is  %s" % `run.state`
        assert run.started != None, "stated should  when it should not be set but is %s" % `run.started`
        assert run.ended == None, "ended when it should not be set but is %s" % `run.ended`
        assert run.errors == '', "Errors should not be set  but is %s" % `run.errors`
        assert job.enabled == True, "Should be enabled but is %s" % job.enabled
        assert job.latest == run, "last run should be completed %s" % run

    # def test_creating_a_run(self):
    #     job =  models.Job.objects.create(
    #         label = label,
    #         description = 'a test job for testing slug'
    #     )
    #     run = models.Run.objects.create(
    #             job = models.ForeignKey('Job')
    #             started = models.DateTimeField(auto_now_add=True)
    #             ended = models.DateTimeField(null=True)
    #             state  = models.CharField(max_length=1, choices= map(lambda x: (x[0],x), (STATUS_PENDING,STATUS_RUNNING, STATUS_COMPLETED, STATUS_ABORTED)), default = STATUS_PENDING)
    #             errors  = models.TextField(default='')
    #         )
    #     assert run.job == job, "job was not set for run %s" % run.pk
    #     assert run.state == run.STATUS_RUNNING, "state not switcted to running %s" % run.state
    #     assert run.started != None, "stated should  when it should not be set %s" % run.ended
    #     assert run.ended == None, "ended when it should not be set %s" % run.ended
    #     assert run.errors == None, "Errors should not be set %s" % run.errors




    def tearDown(self):
        pass
