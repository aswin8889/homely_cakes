from django.shortcuts import render,redirect
from .models import* 
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import datetime
# Create your views here.

####################### COMMON BASE #######################################

def index(request):

    return render(request,'index.html')

def login(request):

    if request.POST:
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(username=email,password=password)

        if user:
            if user.is_active:
                if user.is_superuser:
                    return redirect('/adminhome')
                elif user.usertype=='baker':
                    request.session["email"]=email
                    b=RegistrationBaker.objects.get(email=email)
                    request.session["id"]=b.id
                    return redirect('/bakerhome')
                elif user.usertype=='user':
                    request.session["email"]=email
                    u=RegistrationUser.objects.get(email=email)
                    request.session["id"]=u.id
                    return redirect('/userhome')

    return render(request,"login.html")

def registration_user(request):

    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        contact=request.POST['contact']
        email=request.POST['email']
        password=request.POST['password']

        messages.info(request, "Registration successful")
        
        log=Logintbl.objects.create_user(username=email,password=password,usertype='user')
        log.save()

        data=RegistrationUser.objects.create(name=name,address=address,contact=contact,email=email,userId=log)
        data.save()

    return render(request,'registration_user.html')

def registration_baker(request):

    if request.POST:
        name=request.POST['name']
        b_name=request.POST['b_name']
        profile=request.FILES['profile']
        address=request.POST['address']
        contact=request.POST['contact']
        email=request.POST['email']
        password=request.POST['password']

        messages.info(request, "Registration successful")

        log=Logintbl.objects.create_user(username=email,password=password,usertype='baker')
        log.save()

        data=RegistrationBaker.objects.create(name=name,b_name=b_name,profile=profile,address=address,contact=contact,email=email,bakerId=log)
        data.save()


    return render(request,'registration_baker.html')

########################## ADMIN BASE ######################################################

def adminhome(request):

    return render(request,"admin/adminhome.html")

def manage_bakers(request):

    data=RegistrationBaker.objects.all()

    return render(request,"admin/manage_bakers.html",{'data':data})

def deletebakers(request):
    bid=request.GET.get('id')
    # data=RegistrationBaker.objects.get(id=bid)
    b=Logintbl.objects.get(id=bid)
    b.delete()
    messages.info(request, "Removed successfully")
    return redirect('/manage_bakers')

def manage_users(request):

    data=RegistrationUser.objects.all()

    return render(request,"admin/manage_users.html",{'data':data})

def deleteusers(request):

    id=request.GET.get('id')
    uid=RegistrationUser.objects.get(id=id)

    u=Logintbl.objects.get(id=uid)

    u.delete()
    messages.info(request, "Removed successfully")
    return redirect(request,'/manage_users')

def view_feedback(request):

    feedback=Feedback.objects.all()

    return render(request,"admin/view_feedback.html",{"feedback":feedback})

######################## BAKER BASE #########################################################

def bakerhome(request):

    id =request.session['id']
    baker=RegistrationBaker.objects.get(id=id)

    return render(request,"baker/bakerhome.html",{"baker":baker})


def addcake(request):

    id = request.session['id']
    bakerId=RegistrationBaker.objects.get(id=id)
    
    if request.POST:
        c_name=request.POST['c_name']
        desc=request.POST['desc']
        quantity=request.POST['quantity']
        image=request.FILES['image']
        price=request.POST['price']

        messages.info(request,'Added Sucessesfully')

        cake=AddCakes.objects.create(c_name=c_name,desc=desc,quantity=quantity,image=image,price=price,bakerId=bakerId)
        cake.save()

    return render(request,"baker/addcake.html")

def viewcakebaker(request):

    id = request.session['id']
    cakes=AddCakes.objects.filter(bakerId=id)

    return render(request,"baker/viewcake.html",{"cakes":cakes})

def updatecake(request):

    cid=request.GET.get('id')
    cake=AddCakes.objects.get(id=cid)

    if request.POST:

        c_name=request.POST['c_name']
        cake.c_name=c_name
        desc=request.POST['desc']
        cake.desc=desc
        image=request.FILES['image']
        cake.image=image
        price=request.POST['price']
        cake.price=price
        quantity=request.POST['quantity']
        cake.quantity=quantity
        cake.save()
        messages.info(request, "Successfully updated ")

        return redirect("/viewcakebaker")

    return render(request,"baker/updatecake.html",{'cake':cake})

def deletecake(request):

    cid=request.GET.get('id')
    cake=AddCakes.objects.get(id=cid)
    cake.delete()
    messages.info(request, "Successfully Removed ")

    return redirect("/viewcakebaker")

def viewrequest_baker(request):
    id = request.session['id']
    bakerId=RegistrationBaker.objects.get(id=id)
    requests=Request.objects.filter(bakerId=bakerId)

    return render(request,"baker/viewrequest_baker.html",{"requests":requests})

def accept_order(request):

    rid=request.GET.get('id')
    r=Request.objects.get(id=rid)
    r.status = "Accepted"
    r.save()
    messages.info(request,"Accepted")
    return redirect("/viewrequest_baker")

def reject_order(request):
    rid=request.GET.get('id')
    r=Request.objects.get(id=rid)
    r.status = "Rejected"
    r.save()
    messages.info(request,"Rejected")
    return redirect("/viewrequest_baker")

def message_user(request):
    rid=request.GET.get('id')
    requestId=Request.objects.get(id=rid)
    if request.POST:
        message=request.POST["message"]
        date=datetime.now()
        messages.info(request,"Message sent sucessfully")

        m=Message.objects.create(message=message,date=date,requestId=requestId)
        m.save()

    return render(request,"baker/message_user.html",)

def view_message_baker(request):

    id=request.session['id']
    bakerId=RegistrationBaker.objects.get(id=id)
    msg=Message.objects.filter(requestId__bakerId=bakerId)

    return render(request,"baker/view_message_baker.html",{"msg":msg})

def viewbooking_baker(request):

    id = request.session['id']
    booking=Booking.objects.filter(bakerId=id)

    return render(request,"baker/viewbooking.html",{"booking":booking})


######################  USER HOME #############################################################
def userhome(request):

    id = request.session['id']

    user=RegistrationUser.objects.get(id=id)

    return render(request,"user/userhome.html",{"user":user})

def viewcakesuser(request):

    id = request.session['id']
    cakes=AddCakes.objects.all()

    return render(request,"user/viewcakesuser.html",{"cakes":cakes})

def requestcake(request):

    bid=request.GET.get('id')
    bakerId=RegistrationBaker.objects.get(id=bid)
    id=request.session['id']
    userId=RegistrationUser.objects.get(id=id)

    if request.POST:
        flavour=request.POST['flavour']
        desc=request.POST['desc']
        date=request.POST['date']
        time=request.POST['time']
        quantity=request.POST['quantity']
        current_date=datetime.now()

        messages.info(request,'Request successfully')

        requests=Request.objects.create(flavour=flavour,desc=desc,date=date,time=time,
        quantity=quantity,current_date=current_date,bakerId=bakerId,userId=userId)

        requests.save()

    
    return render(request,"user/requestcakes.html")

def viewbakers_user(request):

    bakers=RegistrationBaker.objects.all()

    return render(request,"user/viewbakers_user.html",{"bakers":bakers} )


def userbooking(request):
    id=request.GET.get('id')
    cakeId=AddCakes.objects.get(id=id)
    bakerId=cakeId.bakerId.id
    bid=RegistrationBaker.objects.get(id=bakerId)
    uid=request.session['id']
    userId=RegistrationUser.objects.get(id=uid)


    if request.POST:
        desc=request.POST['desc']
        current_date=datetime.now()

        book=Booking.objects.create(desc=desc,current_date=current_date,userId=userId,cakeId=cakeId,bakerId=bid)
        book.save()
        return redirect("/payment")

    return render(request,"user/booking.html",{"cid":cakeId})

def viewrequests_user(request):

    id = request.session['id']
    uid=RegistrationUser.objects.get(id=id)
    requests=Request.objects.filter(userId=uid)

    return render(request,"user/viewrequests_user.html",{"requests":requests})

def view_message_user(request):

    id=request.session['id']
    bakerId=RegistrationUser.objects.get(id=id)
    msg=Message.objects.filter(requestId__userId=bakerId)

    return render(request,"user/view_messages_user.html",{"msg":msg})

def payment(request):
    uid=request.session['id']
    userId=RegistrationUser.objects.get(id=uid)
    if request.POST:
        name=request.POST['name']
        current_date=datetime.now()
        payment=Payment.objects.create(name=name,current_date=current_date,userId=userId)
        payment.save()
        return redirect("/viewbooking_user")
    return render(request,"user/payment.html")

def viewbooking_user(request):
    id=request.session['id']
    booking=Booking.objects.filter(userId=id)

    return render(request,"user/viewbooking_user.html",{"booking":booking})

def cancelbooking(request):
    id=request.GET.get('id')
    book=Booking.objects.get(id=id)
    book.status = "Cancelled"
    book.save()

    return redirect("/viewbooking_user")

def feedback(request):
    id=request.GET.get('id')
    bookId=Booking.objects.get(id=id)

    if request.POST:
        title=request.POST['title']
        feedback=request.POST['feedback']
        rating=request.POST['rating']
        current_date=datetime.now()
        
        messages.info(request,'Feedback sent Sucessesfully')
        feed=Feedback.objects.create(title=title,feedback=feedback,rating=rating,current_date=current_date,bookId=bookId)
        feed.save()
        return redirect("/viewbooking_user")
    
    return render(request,"user/feedback.html")