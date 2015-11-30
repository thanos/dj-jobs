# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# (c)2015  thanos vassilakis
#

from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField

class Job(models.Model):
    TYPE_PENDING = 'AD HOC JOB'
    TYPE_CRON = 'CRON JOB'
    TYPE_SERVICE = 'SERVICE'
    label = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from='label')
    description = models.CharField(max_length=255)
    run_type = models.CharField(max_length=1, choices= map(lambda x: (x[0],x), (TYPE_PENDING,TYPE_CRON, TYPE_SERVICE)), default = TYPE_CRON)
    enabled = models.BooleanField(default=False)

    def start(self):
        self.enabled = True
        self.save()
        return Run.objects.create(
                job = self
            )

    @property
    def last_run(self):
        return self.run.latest('ended')
    
    @property
    def running(self):
        return self.run_set.filter(state = Run.STATUS_RUNNING)
        
    @property
    def latest(self):
        return self.running.latest('ended')
    @property
    def run(self):
        return self.run_set.filter(state__ne = Run.STATUS_RUNNING)
    
class Run(models.Model):
    STATUS_RUNNING = 'RUNNING'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_ABORTED = 'ABORTED'
    job = models.ForeignKey('Job')
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)
    state  = models.CharField(max_length=1, choices= map(lambda x: (x[0],x), (STATUS_RUNNING, STATUS_COMPLETED, STATUS_ABORTED)), default = STATUS_RUNNING)
    errors  = models.TextField(default='')



    
