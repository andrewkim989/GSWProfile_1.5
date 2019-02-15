from django.conf.urls import url
from . import views   

urlpatterns = [
    url(r'^$', views.home), # Homepage 
    url(r'^signin$', views.signin), # Signin page 
    url(r'^reg_process$', views.reg_process), 
    url(r'^log_process$', views.log_process),
    url(r'^profile$', views.profile), # User Homepage 
    url(r'^logout$', views.logout),
    url(r'^addplayer$', views.addplayer), # Add a new entry for player 
    url(r'^addcoach$', views.addcoach), # for coach 
    url(r'^addother$', views.addother), # and for other members of the organization 
    url(r'^addplayer_process$', views.addplayer_process),
    url(r'^addcoach_process$', views.addcoach_process),
    url(r'^addother_process$', views.addother_process),
    url(r'^player/(?P<num>\d+)$', views.player), # num is id number
    url(r'^coach/(?P<num>\d+)$', views.coach),
    url(r'^other/(?P<num>\d+)$', views.other),
    url(r'^editplayer/(?P<num>\d+)$', views.editplayer), # num is id number
    url(r'^editcoach/(?P<num>\d+)$', views.editcoach),
    url(r'^editother/(?P<num>\d+)$', views.editother),
    url(r'^editplayer_process/(?P<num>\d+)$', views.editplayer_process), # num is id number
    url(r'^editcoach_process/(?P<num>\d+)$', views.editcoach_process),
    url(r'^editother_process/(?P<num>\d+)$', views.editother_process),
    url(r'^comment_player/(?P<num>\d+)$', views.comment_player), # num is id number
    url(r'^comment_coach/(?P<num>\d+)$', views.comment_coach),
    url(r'^comment_other/(?P<num>\d+)$', views.comment_other),
    url(r'^reply_player/(?P<num>\d+)/(?P<num2>\d+)$', views.reply_player), # num is id number; num2 is comment number
    url(r'^reply_coach/(?P<num>\d+)/(?P<num2>\d+)$', views.reply_coach),
    url(r'^reply_other/(?P<num>\d+)/(?P<num2>\d+)$', views.reply_other),
    url(r'^player_commentlike/(?P<num>\d+)/(?P<num2>\d+)$', views.player_commentlike), # num is id number; num2 is comment number
    url(r'^coach_commentlike/(?P<num>\d+)/(?P<num2>\d+)$', views.coach_commentlike),
    url(r'^other_commentlike/(?P<num>\d+)/(?P<num2>\d+)$', views.other_commentlike),
    url(r'^player_replylike/(?P<num>\d+)/(?P<num2>\d+)$', views.player_replylike), 
    url(r'^coach_replylike/(?P<num>\d+)/(?P<num2>\d+)$', views.coach_replylike), 
    url(r'^other_replylike/(?P<num>\d+)/(?P<num2>\d+)$', views.other_replylike),
    url(r'^player_commentdelete/(?P<num>\d+)/deletecomment/(?P<num2>\d+)$', views.player_commentdelete), # num is id number; num2 is comment number
    url(r'^player_replydelete/(?P<num>\d+)/deletereply/(?P<num2>\d+)$', views.player_replydelete),
    url(r'^coach_commentdelete/(?P<num>\d+)/deletecomment/(?P<num2>\d+)$', views.coach_commentdelete),
    url(r'^coach_replydelete/(?P<num>\d+)/deletereply/(?P<num2>\d+)$', views.coach_replydelete),
    url(r'^other_commentdelete/(?P<num>\d+)/deletecomment/(?P<num2>\d+)$', views.other_commentdelete),
    url(r'^other_replydelete/(?P<num>\d+)/deletereply/(?P<num2>\d+)$', views.other_replydelete),
    url(r'^user/(?P<num>\d+)$', views.userprofile), # View your profile or other user's profile
    url(r'^useractivities/(?P<num>\d+)/page/(?P<num2>\d+)$', views.useractivities),
    url(r'^editprofile$', views.edit), # Edit your profile 
    url(r'^editprofile_process$', views.edit_process),
    url(r'^playercomments/(?P<num>\d+)$', views.playercomments), # Comments in player page
    url(r'^coachcomments/(?P<num>\d+)$', views.coachcomments),
    url(r'^othercomments/(?P<num>\d+)$', views.othercomments),
    url(r'^oops$', views.oops)
]