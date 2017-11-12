from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wypeak.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitterwaves/*', 'wypeak.views.waves'),
    url(r'^oauthLogin/*', 'wypeak.views.oauth_loginDance'),
    url(r'^oauth_helper/*', 'wypeak.views.oauth_helper'),
    url(r'^exportReport/*', 'wypeak.views.exportData'),
    url(r'^isAlive/*', 'wypeak.views.isAlive'),
    url(r'^tweetBuzz/*', 'wypeak.views.wave_service'),
    url(r'^topTweeters/*', 'wypeak.views.wave_topTweeters'),
    url(r'^status/*', 'wypeak.views.get_rate_status'),
    url(r'^search/*', 'wypeak.views.search'),
    url(r'^trends/*', 'wypeak.views.twitter_trends'),
    url(r'^pinsights/*','wypeak.views.getPersonInsights'),
    url(r'^delete_request/*', 'wypeak.views.delete_request'),
    url(r'^add_request/*', 'wypeak.views.add_request'),
    url(r'^delete_query/*', 'wypeak.views.delete_query'),
    url(r'^read_from_db/*', 'wypeak.views.read_from_db')

)

