from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from polls import views

urlpatterns = patterns('',
                       # ex: /polls/
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^signup/$', views.signup, name='signup'),
                       # ex: /polls/5/
                       url(r'^(?P<poll_id>\d+)/$',
                           views.detail, name='detail'),
                       url(r'^(?P<poll_id>\d+)/load_comments$',
                           views.load_comments, name='load_comments'),
                       # ex: /polls/5/vote/
                       url(r'^(?P<poll_id>\d+)/vote/$',
                           views.vote, name='vote'),
                       url(r'^(?P<poll_id>\d+)/(?P<text_comment>[-\w\W]+)/post_comment/$',
                           views.post_comment, name='post_comment'),
                       url(r'^(?P<poll_id>\d+)/post_comment1/$',
                           views.post_comment1, name='post_comment1'),
                       url(r'^(?P<poll_id>\d+)/ajaxvote/$',
                           'polls.views.ajax_vote'),

                       url(r'^(?P<poll_id>\d+)/login/$',
                           views.login, name='login'),
                       url(r'^(?P<poll_id>\d+)/(?P<comment_text>[-\w\W]+)/login1/$',
                           views.login1, name='login1'),
                       url(r'^login/$', views.login2, name='login2'),
                       url(r'^(?P<poll_id>\d+)/(?P<comment_text>[-\w\W]+)/auth_view/$',
                           views.auth_view, name='auth_view'),
                       url(r'^auth1/$', views.auth_view1, name='auth_view1'),
                       url(r'^logout/$', views.logout, name='logout'),


                       url(r'^(?P<poll_id>\d+)/(?P<comment_text>[-\w\W]+)/register_user/$',
                           views.register_user, name='register_user'),
                       url(r'^register_user1/$', views.register_user1,
                           name='register_user1'),

                       url(r'^(?P<user_id>\d+)/manage_account/$',
                           views.manage_account, name='manage_account'),
                       url(r'^delete_account/$', views.delete_account,
                           name='delete_account'),

                       url(r'^forgotpass/$', views.forgotpass,
                           name='forgotpass'),
                       url(r'^send_forgotpass/$', views.send_forgotpass,
                           name='send_forgotpass'),

                       url(r'^(?P<user_id>\d+)/password_reset/$',
                           views.password_reset, name='password_reset'),
                       url(r'^(?P<user_id>\d+)/password_update/$',
                           views.password_update, name='password_update'),


                       url(r'^passreset/$', auth_views.password_reset,
                           name='forgot_password1'),
                       url(r'^passresetdone/$', auth_views.password_reset_done,
                           name='forgot_password2'),
                       url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',
                           auth_views.password_reset_confirm, name='forgot_password3'),
                       url(r'^passresetcomplete/$', auth_views.password_reset_complete,
                           name='forgot_password4'),

                       url(r'^password/change/$', auth_views.password_change,
                           name='auth_password_change'),
                       url(r'^password/change/done/$', auth_views.password_change_done,
                           name='auth_password_change_done'),

                       url(r'^(?P<t_id>[\w\W]+)/verification/$',
                           views.verification, name='verification'),

                       url(r'^(?P<user_id>[\w\W]+)/post_ratings/$',
                           views.post_ratings, name='post_ratings'),

                       url(r'^allusers/$', views.allusers, name='allusers'),

                       url(r'^(?P<user_id>\d+)/profile/$',
                           views.profile, name='profile'),
                       #url(r'^/expired/$',views.expired, name='expired'),

                       #url(r'^admin_login/$', views.admin_login, name='admin_login'),
                       )
