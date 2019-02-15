from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from time import localtime, strftime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Coach, Player, Other, Comment, Reply, Activity

#Homepage

def home(request):
    if not request.session.keys():
        request.session["login"] = "logout"
    context = {
        "players": Player.objects.all(),
        "coaches": Coach.objects.all(),
        "others": Other.objects.all(),
    }
    return render (request, "home.html", context)

#Login & Register

def signin(request):
    if request.session["login"] == "login":
        return redirect("/profile")
    else:
        return render(request, "signin.html")

#Registration process

def reg_process(request):
    if request.method == "POST":
        errors = User.objects.register_validate(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "register")
            return redirect("/signin")
        else: 
            request.session["login"] = "login"
            p = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST["first_name"],
            last_name = request.POST["last_name"], email = request.POST["email"],
            password = p)

            request.session["id"] = user.id
            return redirect("/profile")

#Login process

def log_process(request):
    if request.method == "POST":
        errors = User.objects.login_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "login")
            return redirect("/signin")
        else:
            request.session["login"] = "login"
            user = User.objects.filter(email = request.POST["email"])[0]
            request.session["id"] = user.id

            return redirect("/profile")

#User's homepage

def profile(request):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else: 
        user = User.objects.get(id = request.session["id"])
        all_users = User.objects.all()
        activities = Activity.objects.all().order_by("-id")[:5]
        info = {
            "u": user,
            "users": all_users,
            "activities": activities,
        }
        return render(request, "profile.html", info)

#Logout and clear session

def logout(request):
    request.session["login"] = "logout"
    return redirect("/")

#Add player page

def addplayer(request):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else: 
        return render(request, "addplayer.html")

#Adding new player

def addplayer_process(request):
    if request.method == "POST":
        errors = User.objects.player_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "player")
            return redirect("/addplayer")
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            player = Player.objects.create(name = request.POST["name"],
            image = request.POST["image"], birth_month = request.POST["birth_month"],
            birth_day = request.POST["birth_day"], birth_year = request.POST["birth_year"],
            height_foot = request.POST["height_foot"], height_inches = request.POST["height_inches"],
            weight = request.POST["weight"], position = request.POST["position"],
            previous_teams = request.POST["previous_teams"], college = request.POST["college"],
            draft = request.POST["draft"], jersey = request.POST["jersey"],
            playfrom = request.POST["playfrom"], playto = request.POST["playto"],
            info = request.POST["info"], description = request.POST["description"],
            player_creator = user)
            Activity.objects.create(activity = "Created the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
            return redirect("/player/" + str(player.id))
    
#Player profile page 

def player(request, num):
    player = Player.objects.get(id = num)
    context = {
         "player": player,
         "num": num
    }
    return render(request, "player.html", context)

#Edit player page

def editplayer(request, num):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        player = Player.objects.get(id = num)
        context = {
            "player": player
        }
        return render(request, "editplayer.html", context)

#Editing player

def editplayer_process(request, num):
    player = Player.objects.get(id = num)
    if request.method == "POST":
        errors = User.objects.player_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "player")
            return redirect("/editplayer/" + str(player.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            player.name = request.POST["name"]
            player.image = request.POST["image"]
            player.birth_month = request.POST["birth_month"]
            player.birth_day = request.POST["birth_day"]
            player.birth_year = request.POST["birth_year"]
            player.height_foot = request.POST["height_foot"]
            player.height_inches = request.POST["height_inches"]
            player.weight = request.POST["weight"]
            player.position = request.POST["position"]
            player.previous_teams = request.POST["previous_teams"]
            player.college = request.POST["college"]
            player.draft = request.POST["draft"]
            player.jersey = request.POST["jersey"]
            player.playfrom = request.POST["playfrom"]
            player.playto = request.POST["playto"]
            player.info = request.POST["info"]
            player.description = request.POST["description"]
            player.save()
            Activity.objects.create(activity = "Edited the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
            return redirect("/player/" + str(player.id))

#Comment on player's page

def comment_player(request, num):
    player = Player.objects.get(id = num)
    if request.method == "POST":
        user = User.objects.get(id = request.session["id"])
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        commenter = User.objects.get(id = request.session["id"])
        c = Comment.objects.create(comment = request.POST["comment"], commenter = commenter)
        player.player_comments.add(c)
        Activity.objects.create(activity = "Commented on the following page: "
        + str(player.name) + " (" + str(t) + ")", act = user)
        return redirect("/playercomments/" + str(player.id))

#Add coach page

def addcoach(request):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        return render(request, "addcoach.html")

#Adding new coach

def addcoach_process(request):
    if request.method == "POST":
        errors = User.objects.coach_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "coach")
            return redirect("/addcoach")
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            coach = Coach.objects.create(name = request.POST["name"],
            image = request.POST["image"], birth_month = request.POST["birth_month"],
            birth_day = request.POST["birth_day"], birth_year = request.POST["birth_year"],
            height_foot = request.POST["height_foot"], height_inches = request.POST["height_inches"],
            weight = request.POST["weight"], position = request.POST["position"],
            teams_played = request.POST["teams_played"],
            teams_coached = request.POST["teams_coached"], college = request.POST["college"],
            draft = request.POST["draft"], playfrom = request.POST["playfrom"],
            playto = request.POST["playto"], coachfrom = request.POST["coachfrom"],
            coachto = request.POST["coachto"], coach_position = request.POST["coach_position"],
            info = request.POST["info"], description = request.POST["description"], coach_creator = user)
            Activity.objects.create(activity = "Created the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
            return redirect("/coach/" + str(coach.id))

#Coach profile page

def coach(request, num):
    coach = Coach.objects.get(id = num)
    context = {
        "coach": coach,
        "num": num
    }
    return render(request, "coach.html", context)

#Edit coach page

def editcoach(request, num):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        coach = Coach.objects.get(id = num)
        context = {
            "coach": coach
        }
        return render(request, "editcoach.html", context)

#Editing coach profile

def editcoach_process(request, num):
    coach = Coach.objects.get(id = num)
    if request.method == "POST":
        errors = User.objects.coach_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "coach")
            return redirect("/editcoach/" + str(coach.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            coach.name = request.POST["name"]
            coach.image = request.POST["image"]
            coach.birth_month = request.POST["birth_month"]
            coach.birth_day = request.POST["birth_day"]
            coach.birth_year = request.POST["birth_year"]
            coach.height_foot = request.POST["height_foot"]
            coach.height_inches = request.POST["height_inches"]
            coach.weight = request.POST["weight"]
            coach.position = request.POST["position"]
            coach.teams_played = request.POST["teams_played"]
            coach.teams_coached = request.POST["teams_coached"]
            coach.college = request.POST["college"]
            coach.draft = request.POST["draft"]
            coach.playfrom = request.POST["playfrom"]
            coach.playto = request.POST["playto"]
            coach.coachfrom = request.POST["coachfrom"]
            coach.coachto = request.POST["coachto"]
            coach.coach_position = request.POST["coach_position"]
            coach.info = request.POST["info"]
            coach.description = request.POST["description"]
            coach.save()
            Activity.objects.create(activity = "Edited the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
            return redirect("/coach/" + str(coach.id))

#Commenting on coach profile page

def comment_coach(request, num):
    coach = Coach.objects.get(id = num)
    if request.method == "POST":
        user = User.objects.get(id = request.session["id"])
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        commenter = User.objects.get(id = request.session["id"])
        c = Comment.objects.create(comment = request.POST["comment"], commenter = commenter)
        coach.coach_comments.add(c)
        Activity.objects.create(activity = "Commented on the following page: "
        + str(coach.name) + " (" + str(t) + ")", act = user)
        return redirect("/coachcomments/" + str(coach.id))

#Add other page    

def addother(request):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        return render(request, "addother.html")

#Adding other members of the organization

def addother_process(request):
    if request.method == "POST":
        errors = User.objects.other_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "other")
            return redirect("/addother")
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            other = Other.objects.create(name = request.POST["name"],
            image = request.POST["image"], birth_month = request.POST["birth_month"],
            birth_day = request.POST["birth_day"], birth_year = request.POST["birth_year"],
            height_foot = request.POST["height_foot"], height_inches = request.POST["height_inches"],
            weight = request.POST["weight"], position = request.POST["position"],
            info = request.POST["info"], description = request.POST["description"], other_creator = user)
            Activity.objects.create(activity = "Created the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
            return redirect("/other/" + str(other.id))

#Other page

def other(request, num):
    o = Other.objects.get(id = num)
    context = {
        "other": o,
        "num": num
    }
    return render(request, "other.html", context)

#Edit other page

def editother(request, num):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        other = Other.objects.get(id = num)
        context = {
            "other": other
        }
        return render(request, "editother.html", context)

#Editing pages belonging to other members of the organization

def editother_process(request, num):
    other = Other.objects.get(id = num)
    if request.method == "POST":
        errors = User.objects.other_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "other")
            return redirect("/editother/" + str(other.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
            user = User.objects.get(id = request.session["id"])
            other.name = request.POST["name"]
            other.image = request.POST["image"]
            other.birth_month = request.POST["birth_month"]
            other.birth_day = request.POST["birth_day"]
            other.birth_year = request.POST["birth_year"]
            other.height_foot = request.POST["height_foot"]
            other.height_inches = request.POST["height_inches"]
            other.weight = request.POST["weight"]
            other.position = request.POST["position"]
            other.info = request.POST["info"]
            other.description = request.POST["description"]
            other.save()
            Activity.objects.create(activity = "Edited the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
            return redirect("/other/" + str(other.id))

#Commenting on profile pages of other members of the organization

def comment_other(request, num):
    other = Other.objects.get(id = num)
    if request.method == "POST":
        user = User.objects.get(id = request.session["id"])
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        commenter = User.objects.get(id = request.session["id"])
        c = Comment.objects.create(comment = request.POST["comment"], commenter = commenter)
        other.other_comments.add(c)
        Activity.objects.create(activity = "Commented on the following page: "
        + str(other.name) + " (" + str(t) + ")", act = user)
        return redirect("/othercomments/" + str(other.id))

#Liking a comment on a player's profile page

def player_commentlike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        if exists: 
            return redirect("/playercomments/" + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = "Liked a comment on the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
            return redirect("/playercomments/" + num)

#Liking a comment on a coach's profile page

def coach_commentlike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        if exists: 
            return redirect("/coachcomments/" + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = "Liked a comment on the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
            return redirect("/coachcomments/" + num)

#Liking a comment on other members of the organization's profile page

def other_commentlike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        if exists: 
            return redirect("/othercomments/" + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = "Liked a comment on the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
            return redirect("/othercomments/" + num)

#Replying to a comment on a player's profile page

def reply_player(request, num, num2):
    player = Player.objects.get(id = num)
    if request.method == "POST":
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        post = Comment.objects.get(id = num2)
        reply_user = User.objects.get(id = request.session["id"])
        r = Reply.objects.create(reply = request.POST["reply"], replier = reply_user, comment = post)
        player.player_replies.add(r)
        Activity.objects.create(activity = "Replied to a user on the following page: "
        + str(player.name) + " (" + str(t) + ")", act = reply_user)
        return redirect("/playercomments/" + str(player.id))

#Replying to a comment on a coach's profile page

def reply_coach(request, num, num2):
    coach = Coach.objects.get(id = num)
    if request.method == "POST":
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        post = Comment.objects.get(id = num2)
        reply_user = User.objects.get(id = request.session["id"])
        r = Reply.objects.create(reply = request.POST["reply"], replier = reply_user, comment = post)
        coach.coach_replies.add(r)
        Activity.objects.create(activity = "Replied to a user on the following page: "
        + str(coach.name) + " (" + str(t) + ")", act = reply_user)
        return redirect("/coachcomments/" + str(coach.id))

#Replying to a comment on other members of the organization's profile page

def reply_other(request, num, num2):
    other = Other.objects.get(id = num)
    if request.method == "POST":
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        post = Comment.objects.get(id = num2)
        reply_user = User.objects.get(id = request.session["id"])
        r = Reply.objects.create(reply = request.POST["reply"], replier = reply_user, comment = post)
        other.other_replies.add(r)
        Activity.objects.create(activity = "Replied to a user on the following page: "
        + str(other.name) + " (" + str(t) + ")", act = reply_user)
        return redirect("/othercomments/" + str(other.id))

#Liking a reply on a player's profile page

def player_replylike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect("/playercomments/" + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = "Liked a reply on the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
            return redirect("/playercomments/" + num)

#Liking a reply on a coach's profile page

def coach_replylike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect("/coachcomments/" + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = "Liked a reply on the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
            return redirect("/coachcomments/" + num)

#Liking a reply on other members of the organization's profile page

def other_replylike(request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect("/othercomments/" + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = "Liked a reply on the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
            return redirect("/othercomments/" + num)

#Deleting a comment on player's profile page

def player_commentdelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        c.delete()
        Activity.objects.create(activity = "Deleted a comment on the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
        return redirect("/playercomments/" + num)

#Deleting a reply on player's profile page

def player_replydelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        r.delete()
        Activity.objects.create(activity = "Deleted a reply on the following page: "
            + str(player.name) + " (" + str(t) + ")", act = user)
        return redirect("/playercomments/" + num)

#Deleting a comment on coach's profile page

def coach_commentdelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        c.delete()
        Activity.objects.create(activity = "Deleted a comment on the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
        return redirect("/coachcomments/" + num)

#Deleting a reply on coach's profile page

def coach_replydelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        r.delete()
        Activity.objects.create(activity = "Deleted a reply on the following page: "
            + str(coach.name) + " (" + str(t) + ")", act = user)
        return redirect("/coachcomments/" + num)

#Deleting a comment on other members of the organization's profile page

def other_commentdelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        c = Comment.objects.get(id = num2)
        c.delete()
        Activity.objects.create(activity = "Deleted a comment on the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
        return redirect("/othercomments/" + num)

#Deleting a reply on other members of the organization's profile page

def other_replydelete (request, num, num2):
    if request.session["login"] == "logout":
        return redirect("/signin")
    else:
        t = strftime("%B/%d/%Y, %I:%M %p %Z", localtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session["id"])
        r = Reply.objects.get(id = num2)
        r.delete()
        Activity.objects.create(activity = "Deleted a reply on the following page: "
            + str(other.name) + " (" + str(t) + ")", act = user)
        return redirect("/othercomments/" + num)

#User profile

def userprofile (request, num):
    u = User.objects.get(id = num)
    context = {
        "u": u,
        "num": num
    }
    return render(request, "user.html", context)

#User's activities

def useractivities (request, num, num2):
    u = User.objects.get(id = num)
    activities = Activity.objects.filter(act = u).order_by("-created_at")

    page = request.GET.get("page", num2)

    paginator = Paginator(activities, 8)
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)

    context = {
        "u": u,
        "activities": activities,
        "num": num
    }

    return render(request, "activities.html", context)

#Edit page for user

def edit(request):
    if request.session["login"] == "logout":
        return redirect("/oops")
    else:
        user = User.objects.get(id = request.session["id"])
        context = {
            "user": user
        }
        return render (request, "edit.html", context)

#Editing own user's profile

def edit_process(request):
    user = User.objects.get(id = request.session["id"])

    if request.method == "POST":
        errors = User.objects.edit_validate(request.POST, user)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = "edit")
            return redirect("/editprofile")
        else:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()
        return redirect("/profile")

#Comments and replies in a player's profile page

def playercomments(request, num):
    a = 0
    player = Player.objects.get(id = num)
    comments = Comment.objects.filter(player_commented = player)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
        "player": player,
        "comments": comments,
        "all": a,
    }
    return render(request, "playercomments.html", context)

#Comments and replies in a coach's profile page

def coachcomments(request, num):
    a = 0
    coach = Coach.objects.get(id = num)
    comments = Comment.objects.filter(coach_commented = coach)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
        "coach": coach,
        "comments": comments,
        "all": a
    }
    return render(request, "coachcomments.html", context)

#Comments and replies in other members of the organization's profile page

def othercomments(request, num):
    a = 0
    o = Other.objects.get(id = num)
    comments = Comment.objects.filter(other_commented = o)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
        "other": o,
        "comments": comments,
        "all": a
    }
    return render(request, "othercomments.html", context)

#Redirect to this page if a person tries to access a page that cannot be accessed without logging in

def oops(request):
    return render(request, "oops.html")

"""
purplesmart@eq.net Twily123
glimglam@eq.net Glimmy25
20cooler@eq.net Dashie20
partypony@eq.net Pinkie30
nightprincess@eq.net Moon0204
sunprincess@eq.net Sunny111
"""