from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator

from access_tokens import scope, tokens

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from polls.models import Poll, Choice, Comment, Vote, Tokens, Ratings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from forms import MyRegistrationForm


import json

from django.utils import simplejson
from django.template.loader import render_to_string
from django.core import serializers

import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

# Create your views here.


def index(request):
    print timezone.now()
    request.session.set_test_cookie()
    request.session.set_test_cookie()
    latest_poll_list = Poll.objects.all()
    if not request.user.is_authenticated():
        ratings = Ratings.objects.filter(
            Q(rate_user=request.META['REMOTE_ADDR']))
        print ratings
    else:
        ratings = Ratings.objects.filter(Q(rate_user=request.user.id))
        print ratings
    context = RequestContext(request, {'request': request, 'latest_poll_list': latest_poll_list,
                                       'full_name': request.user.username, 'user_id': request.user.id, 'ratings': ratings})
    return render_to_response('polls/index.html', context_instance=context)
    #context = {'latest_poll_list': latest_poll_list,'full_name':request.user.username,'user_id':request.user.id,'request':request}
    # return render(request,'polls/index.html',context)


def post(self, request, *args, **kwargs):
    if self.request.is_ajax():
        return self.ajax(request)


def login(request, poll_id):
    #request.session['comment'] = request.POST['comment']
    user_name = request.COOKIES.get('username')
    pass_word = request.COOKIES.get('password')
    comment_text = request.POST['comment']
    print comment_text
    c = {}
    c.update(csrf(request))
    c.update({'comment_text': comment_text})
    poll = get_object_or_404(Poll, pk=poll_id)
    c.update({'poll': poll})
    c.update({'u_name': user_name})
    c.update({'pwd': pass_word})
    return render(request, 'polls/login.html', c)


def login1(request, poll_id, comment_text):
    #request.session['comment'] = request.POST['comment']
    #comment_text = request.POST['comment']
    user_name = request.COOKIES.get('username')
    pass_word = request.COOKIES.get('password')
    print comment_text
    c = {}
    c.update(csrf(request))
    c.update({'comment_text': comment_text})
    poll = get_object_or_404(Poll, pk=poll_id)
    c.update({'poll': poll})
    c.update({'u_name': user_name})
    c.update({'pwd': pass_word})
    return render(request, 'polls/login.html', c)


def login2(request):
    user_name = request.COOKIES.get('username')
    pass_word = request.COOKIES.get('password')

    print user_name
    print pass_word
    print 'hi'
    c = {}
    c.update(csrf(request))
    c.update({'u_name': user_name})
    c.update({'pwd': pass_word})
    return render(request, 'polls/login1.html', c)


def auth_view1(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    try:
        p = User.objects.get(username=username)
    except:
        return render(request, 'polls/login1.html', {
            'error_message': "Login details are invalid, Please correct username and password.",
        })
    print p.is_active
    if user is not None:
        if p.is_active == True:
            auth.login(request, user)
            response = HttpResponseRedirect('/index')
            if request.method == 'POST':
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                    print "checked"
                    if username in request.COOKIES:
                        username = request.COOKIES['username']
                    if password in request.COOKIES:
                        password = request.COOKIES['password']
                else:
                    print "Not Checked"
                    response.set_cookie('username', username)
                    response.set_cookie('password', password)
            return response
        else:
            return render(request, 'polls/login1.html', {
                'error_message': 'Check your Mail and active your account to login.',
            })
    else:
        return render(request, 'polls/login1.html', {
            'error_message': "Login details are invalid, Please correct username and password.",
        })


def auth_view(request, poll_id, comment_text):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    poll = get_object_or_404(Poll, pk=poll_id)
    comment = comment_text
    print comment
    try:
        p = User.objects.get(username=username)
    except:
        return render(request, 'polls/login.html', {
            'poll': poll,
            'comment_text': comment_text,
            'error_message': " Login details are invalid, Please correct username and password.",
        })
    poll = get_object_or_404(Poll, pk=poll_id)
    comment = comment_text
    print comment
    if user is not None:
        if p.is_active == True:
            auth.login(request, user)
            response = HttpResponseRedirect(
                reverse('polls:post_comment', args=(poll.id, comment,)))
            if request.method == 'POST':
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                    if username in request.COOKIES:
                        username = request.COOKIES['username']
                    if password in request.COOKIES:
                        password = request.COOKIES['password']
                else:
                    print "Not Checked"
                    response.set_cookie('username', username)
                    response.set_cookie('password', password)
            return response
        else:
            return render(request, 'polls/login.html', {
                'poll': poll,
                'comment_text': comment_text,
                'error_message': 'Check your Mail and active your account to login.',
            })
    else:
        return render(request, 'polls/login.html', {
            'poll': poll,
            'comment_text': comment_text,
            'error_message': " Login details are invalid, Please correct username and password.",
        })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')


def signup(request):
    if request.method == "GET":
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            post = User.objects.create(
                username=username, email=email, password=password1)
            return HttpResponseRedirect(reverse('signin'))
    return render(request, 'polls/signup.html')


def register_user(request, poll_id, comment_text):
    comment = comment_text
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                is_active = 0
                print is_active

                def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
                    return "".join(random.choice(chars) for _ in range(size))
                print id_generator(size=36)
                form.save()
                print id_generator(size=36)
                token_obj = Tokens(token_id=random(), user_id_id=form.id)
                print "testing"
                token_obj.save()
                print "testing"
                subject = 'Thank you'
                message = 'welcome to polls website, Click here to active your account http://10.90.90.124:8000/index/'
                from_email = settings.EMAIL_HOST_USER
                to_list = [form.email, settings.EMAIL_HOST_USER]
                send_mail(
                    subject, message, from_email, to_list, fail_silently=True)
                return HttpResponseRedirect(reverse('polls:post_comment', args=(poll.id, comment,)))
        except:
            return render(request, 'polls/register.html', {
                'form': form,
                'poll': poll,
                'comment_text': comment_text,
                'error_message': "This Email address already exists.",
            })
    else:
        form = MyRegistrationForm()
    c = {}
    c.update(csrf(request))
    c.update({'form': form})
    c.update({'poll': poll})
    c.update({'comment_text': comment_text})
    return render_to_response('polls/register.html', c)

    args = {}
    args.update(csrf(request))
    args.update({'poll': poll})
    args['form'] = MyRegistrationForm()

    return render_to_response('polls/register.html', args)


def register_user1(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        print form.is_valid()
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                is_active = 0
                print is_active
                form.save()
                print "test"
                x = User.objects.get(username=form.cleaned_data['username'])
                print x.id
                token_obj = Tokens(
                    token_id=id_generator(size=36), user_id_id=x.id)
                print "test6"
                token_obj.save()
                print Tokens.objects.get(user_id_id=x.id)
                print "testing"
                print "test"
                subject = 'Thank you'
                message = 'welcome to polls website ,Click here to active your account http://10.90.90.124:8000/%s/verification/' % Tokens.objects.get(
                    user_id_id=x.id)
                from_email = settings.EMAIL_HOST_USER
                to_list = [form.cleaned_data['email']]
                send_mail(
                    subject, message, from_email, to_list, fail_silently=True)
                print "test5"
                messages.warning(
                    request, 'Please Check your Mail to Activate your Account')
                return HttpResponseRedirect(reverse('polls:index'))
        except:
            return render(request, 'polls/register1.html', {
                'form': form,
                'error_message': "This Email address already exists.",
            })
    else:
        form = MyRegistrationForm()
    c = {}
    c.update(csrf(request))
    c.update({'form': form})
    return render_to_response('polls/register1.html', c)


@login_required(login_url="/index/")
def manage_account(request, user_id):
    a = User.objects.get(pk=user_id)
    print a
    print request.user.social_auth.get(provider='facebook').uid
    print request.user.username
    if request.method == "POST":
        print "test1"
        form = MyRegistrationForm(request.POST, instance=a)
        print "test2"
        # print form.is_valid()
        try:
            if form.is_valid():
                form.save()
                print "test2"
                a.is_active = True
                a.save()
                messages.warning(request, 'Updated successfully')
                return HttpResponseRedirect(reverse('polls:index'))
        except:
            return render(request, 'polls/manage_account.html', {
                'form': form,
                'user_id': a.id,
            })
    else:
        form = MyRegistrationForm()
    c = {}
    c.update(csrf(request))
    c.update({'user_id': a.id})
    c.update({'form': form})
    c.update({'username': a.username})
    c.update({'email': a.email})
    c.update({'first_name': a.first_name})
    c.update({'last_name': a.last_name})
    return render_to_response('polls/manage_account.html', c)


def delete_account(request):
    print "test2"
    a = User.objects.get(id=request.user.id)
    print a
    print "test1"
    a.delete()
    print "test"
    return HttpResponseRedirect('/index')


def detail(request, poll_id):
    latest_poll_list = Poll.objects.all()
    poll = get_object_or_404(Poll, pk=poll_id)
    comments_list = poll.comment_set.all()
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')

    try:
        comment = paginator.page(page)
    except PageNotAnInteger:
        comment = paginator.page(1)
    except EmptyPage:
        comment = paginator.page(paginator.num_pages)
    if timezone.now() < poll.expire_date:
        print 'Polls is in active'
        return render(request, 'polls/detail.html', {'poll': poll, 'comments': comment})
    else:
        print 'poll is in deactive'
        messages.warning(
            request, 'Sorry! Your requesting poll was Expired, Please try another')
        return HttpResponseRedirect(reverse('polls:index'))


def ValuesQuerySetToDict(vqs):
    return [{'object': (item.comment, item.id, item.poll_id, item.user_id, item.username, item.first_name, item.last_name,
                        item.email)} for item in vqs]


def load_comments(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    comments_list = poll.comment_set.all()
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comment = paginator.page(page)
    except PageNotAnInteger:
        comment = paginator.page(1)
    except EmptyPage:
        comment = paginator.page(paginator.num_pages)
    #data = serializers.serialize('json', comment, fields=('comment','poll_id', 'id'))
    data_dict = ValuesQuerySetToDict(comment)
    if comment.has_next():
        num = comment.next_page_number()
    else:
        num = 0
    details = [num, poll_id]
    data_json = simplejson.dumps(data_dict)
    return HttpResponse(simplejson.dumps({"comments": data_json, "details": details}))


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def post_comment(request, poll_id, text_comment):
    print request.user.username
    print request.user.first_name
    print request.user.last_name
    print request.user.email
    print request.user.id
    #p = get_object_or_404(Poll, pk=poll_id)
    p = Poll.objects.get(pk=poll_id)
    try:
        comment_txt = text_comment
    except:
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You Must Type Comment.",
        })
    else:
        comment_obj = Comment(comment=comment_txt, poll_id=poll_id,
                              user_id=request.user.id, username=request.user.username,
                              first_name=request.user.first_name,
                              last_name=request.user.last_name,
                              email=request.user.email,
                              date_joined=request.user.date_joined
                              )
        comment_obj.save()
        q = Comment.objects.all().filter(comment=" ")
        q.delete()
        return HttpResponseRedirect(reverse('polls:detail', args=(p.id,)))


def post_comment1(request, poll_id):
    #p = get_object_or_404(Poll, pk=poll_id)
    print request.user.username
    print request.user.first_name
    print request.user.last_name
    print request.user.email
    p = Poll.objects.get(pk=poll_id)
    try:
        comment_text = request.POST['comment']
    except:
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You Must Type Comment.",
        })
    else:
        comment_obj = Comment(comment=comment_text, poll_id=poll_id,
                              user_id=request.user.id, username=request.user.username,
                              first_name=request.user.first_name,
                              last_name=request.user.last_name,
                              email=request.user.email,
                              date_joined=request.user.date_joined
                              )
        comment_obj.save()
        q = Comment.objects.all().filter(comment=" ")
        q.delete()
        # return render(request,'polls/detail.html',{'poll':p})
        return HttpResponseRedirect(reverse('polls:detail', args=(p.id,)))


def ajax_vote(request, poll_id):
    # if request.session.get('has_voted',False):
        # return HttpResponse("You've already voted")
    p = get_object_or_404(Poll, pk=poll_id)
    print "test1"
    vote_id = Vote.objects.filter(poll_id=poll_id)
    print "test2"
    print vote_id
    if request.user.username:
        vote_user = Vote.objects.filter(
            poll_id=poll_id, user_name=request.user.username)
    else:
        vote_user = Vote.objects.filter(
            poll_id=poll_id, user_name=request.META.get('REMOTE_ADDR'))
    print "test3"
    print vote_user

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        print "test4"
    except (KeyError, Choice.DoesNotExist):
        return HttpResponseServerError("You didn't select a choice to vote")
        print "test4"
    else:
        print "test5"
        if vote_user:
            print "test6"
            if vote_id:
                print "you have submitted vote already"
                return render_to_response('polls/votes.html', {'num_votes': selected_choice.votes}, context_instance=RequestContext(request))
        else:
            print "test"
            if request.user.username:
                print 'test'
                print request.user.username
                print poll_id
                vote_obj = Vote(
                    poll_id=poll_id, user_name=request.user.username)
                vote_obj.save()
            else:
                print 'test2'
                print request.META.get('REMOTE_ADDR')
                print poll_id
                vote_obj = Vote(
                    poll_id=poll_id, user_name=request.META.get('REMOTE_ADDR'))
                vote_obj.save()
            selected_choice.votes += 1
            selected_choice.save()
            #request.session['has_voted'] = True
            num_votes = selected_choice.votes
            print num_votes
            if request.is_ajax():
                return render_to_response('polls/votes.html', {'num_votes': num_votes}, context_instance=RequestContext(request))


def forgotpass(request):
    return render(request, 'polls/forgotpass.html')


def send_forgotpass(request):
    print "test"
    if request.method == "POST":
        print "test1"
        try:
            print "test2"
            email = request.POST['email']
            print "test3"
            print email
            obj = User.objects.get(email=email)
            print "test4"
            print obj.id
            subject = 'Thank you'
            message = 'welcome to polls website ,Click here to Reset Your Password http://10.90.90.124:8000/%d/password_reset/' % obj.id
            print "test5"
            from_email = settings.EMAIL_HOST_USER
            to_list = [obj.email]
            send_mail(
                subject, message, from_email, to_list, fail_silently=True)
            messages.warning(
                request, 'Please Check your Mail We have sent an Email regarding reset Password link')
            print 'test6'
            return HttpResponseRedirect(reverse('polls:index'))
        except:
            return render(request, 'polls/forgotpass.html', {
                'error_message': "This Email address Does not exists in our records.",
            })


def password_reset(request, user_id):
    a = User.objects.get(pk=user_id)
    print 'test'
    c = {}
    c.update(csrf(request))
    c.update({'user_id': a.id})
    c.update({'username': a.username})
    return render_to_response('polls/password_reset.html', c)


def password_update(request, user_id):
    a = User.objects.get(pk=user_id)
    print a.password
    if request.method == "POST":
        print "test1"
        print user_id
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            print "both same"
            a.set_password(pass2)
            a.save()
            return render(request, 'polls/reset_success.html')
        else:
            c = {}
            c.update(csrf(request))
            c.update({'user_id': a.id})
            c.update({'username': a.username})
            c.update(
                {'error_message': 'The Passwords did not match, please enter same'})
            return render(request, 'polls/password_reset.html', c)


def verification(request, t_id):
    try:
        t = Tokens.objects.get(token_id=t_id)
        u = User.objects.get(pk=t.user_id_id)
        u.is_active = True
        u.save()
        t.delete()
        return render(request, 'polls/verification.html')
    except:
        return render(request, 'polls/expired.html')


def post_ratings(request, user_id):
    print 'test'
    print request.META.get('REMOTE_ADDR')
    print request.GET['rating']
    print request.GET['poll_id']
    print user_id
    p_id = request.GET['poll_id']
    rate = request.GET['rating']
    ip = request.META.get('REMOTE_ADDR')
    if user_id == 'None':
        try:
            u = Ratings.objects.filter(
                rate_user=request.META.get('REMOTE_ADDR'))
            p = Ratings.objects.filter(
                Q(poll_id=p_id) & Q(rate_user=request.META.get('REMOTE_ADDR')))
            if u:
                for i in u:
                    print i.rate_user
                    if i.rate_user == request.META.get('REMOTE_ADDR'):
                        print 'user exists '
                        if p:
                            for j in p:
                                if j.rate_user == request.META.get('REMOTE_ADDR'):
                                    print 'store only rating'
                                    j.rating = rate
                                    j.save()
                                    break
                                else:
                                    print 'store'
                            print j.poll_id
                        else:
                            print 'store with poll_id'
                            rating_obj = Ratings(
                                poll_id=p_id, rate_user=request.META.get('REMOTE_ADDR'), rating=rate)
                            rating_obj.save()
                            break
                        break
            else:
                print 'store with all'
                rating_obj = Ratings(
                    poll_id=p_id, rate_user=request.META.get('REMOTE_ADDR'), rating=rate)
                rating_obj.save()

        except:
            print 'not exists'
    else:
        try:
            u = Ratings.objects.filter(rate_user=user_id)
            p = Ratings.objects.filter(Q(poll_id=p_id) & Q(rate_user=user_id))
            print 'test worked'
            if u:
                for i in u:
                    print i.rate_user
                    if i.rate_user == user_id:
                        print 'user exists'
                        if p:
                            for j in p:
                                if j.rate_user == user_id:
                                    print 'store only rating'
                                    print j.rating
                                    j.rating = rate
                                    j.save()
                                    print rate
                                    break
                                else:
                                    print 'store'
                            print j.poll_id
                        else:
                            print 'store with poll_id'
                            rating_obj = Ratings(
                                poll_id=p_id, rate_user=user_id, rating=rate)
                            rating_obj.save()
                            break
                        break
            else:
                print 'store with all'
                rating_obj = Ratings(
                    poll_id=p_id, rate_user=user_id, rating=rate)
                rating_obj.save()
        except:
            print 'not exists'
    print p_id
    print rate
    rating_obj.save()
    print 'success'
    return HttpResponseRedirect(reverse('polls:index'))


def allusers(request):
    print 'allusers'
    users = User.objects.all()
    print all
    return render(request, 'polls/allusers.html', {'allusers': users})


def profile(request, user_id):
    print 'profile'
    print user_id
    user_profile = User.objects.get(pk=user_id)
    return render(request, 'polls/profile.html', {'profile': user_profile})
