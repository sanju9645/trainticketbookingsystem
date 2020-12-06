from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from .forms import AgentProfileForm
from .models import Agent
from django.core.files.storage import FileSystemStorage
# Create your views here.

@login_required(login_url="/auth/")
def showProfilePage(request):
    user = request.user
    agent = Agent.objects.filter(user=user)
    context = {'status':0}
    if agent.exists():
        agent = agent.last()
        context = {'status':1,'name':agent.name,
                    'phone':agent.phone,'address':agent.address,
                    'dob':agent.dob,'image':agent.profile_pic}

    return render(request, 'agent-profile.html', context)


@login_required(login_url="/auth/")
def updateProfilePage(request):
    if request.method == "POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        dob=request.POST.get('dob')
        profile_pic=request.POST.get('profilePicture')#name of profile picture

        profile_pic = request.FILES['profilePicture']#profile picture
        fs = FileSystemStorage()    #fs object will interact with file system(hard disk)
        filename = fs.save(profile_pic.name, profile_pic)#MEDIA_ROOT folder

        #print(profile_pic)
        a = Agent.objects.filter(user=request.user)
        if a.exists():
            a = a.last()
            a.user = request.user
            a.name=name
            a.address=address
            a.phone=phone
            a.profile_pic=profile_pic
            a.save()
        # if a:
        #     print("created")
        # else:
        #     print("not created")
        return redirect("showProfile")
        # else:
        #     return redirect("/agent/profile/update?message=Invalid Entries. Try again")
    else:
        #agentForm = AgentProfileForm()
        #return render(request, "update-profile.html", {'form': agentForm})
        return render(request, "update-profile.html", {})