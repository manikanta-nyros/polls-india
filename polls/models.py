from django.db import models
from datetime import date
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from djangoratings.fields import RatingField
from django.db.models import Avg
import math
from django.contrib.sites.models import Site

# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    rating = models.FloatField()
    expire_date = models.DateTimeField("Expired Date")
    #star_rating = LikertField()

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def sort_by_rating(self):
        print timezone.now()
        p1 = Ratings.objects.all().filter(poll_id=1).aggregate(Avg('rating'))
        p2 = Ratings.objects.all().filter(poll_id=2).aggregate(Avg('rating'))
        p3 = Ratings.objects.all().filter(poll_id=3).aggregate(Avg('rating'))
        print 'test1'
        pid1 = Poll.objects.get(pk=1)
        pid2 = Poll.objects.get(pk=2)
        pid3 = Poll.objects.get(pk=3)
        print 'test2'
        pid1.rating = p1['rating__avg']
        pid2.rating = p2['rating__avg']
        pid3.rating = p3['rating__avg']
        print 'test3'
        pid1.save()
        pid2.save()
        pid3.save()
        print 'test4'
        poll1 = Ratings.objects.all().filter(
            poll_id=self).aggregate(Avg('rating'))
        return poll1['rating__avg']
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    sort_by_rating.short_description = 'Ratings for Polls'
    sort_by_rating.admin_order_field = 'rating'

    def get_absolute_url(self):
        return u"/polls/%s/" % self.pk


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    #sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.choice_text


class Comment(models.Model):
    poll = models.ForeignKey(Poll)
    comment = models.CharField(max_length=1000)
    user_id = models.IntegerField(max_length=11)
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    date_joined = models.DateTimeField()

    def __unicode__(self):
        return self.comment

    def save_comment(self, comment_text, poll_id):
        p = Poll.objects.get(pk=poll_id)
        p.comment_set.create(comment=comment_text, poll_id=poll_id)


class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    user_name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user_name


class Tokens(models.Model):
    token_id = models.CharField(max_length=60)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        return self.token_id


class UserProfilePic(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles')

    def __str__(self):
        return "%s's profile" % self.user


class Ratings(models.Model):
    poll = models.ForeignKey(Poll)
    rate_user = models.CharField(max_length=32)
    rating = models.IntegerField(max_length=5)

    def __unicode__(self):
        return self.rate_user


def deactive_poll(self):
    polls = Poll.objects.all()
    print polls
    for poll in polls:
        print poll.pub_date
        print poll.expire_date
        if timezone.now() < poll.expire_date:
            print 'Polls is in active'
            return true
        else:
            print 'poll is in deactive'
            return false
