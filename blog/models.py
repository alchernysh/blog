# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.views.generic.edit import CreateView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils.encoding import force_unicode
# Create your models here.
class Post(models.Model):
    #blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique_for_date = "posted_date", verbose_name = "Заголовок")
    body = RichTextUploadingField(config_name='awesome_ckeditor', verbose_name = "Содержание") #models.TextField(max_length=10000,verbose_name = "")
    description = models.TextField(verbose_name = "Description", blank = True)
    posted_date = models.DateTimeField(default = timezone.now, db_index = True, verbose_name = "Добавлено")
    user = models.ForeignKey(User, editable = True)
    tags = TaggableManager(blank = True, verbose_name = "Теги")

    class Meta:
        ordering = ['posted_date']
        verbose_name ="Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def __str__(self):
        return self.body