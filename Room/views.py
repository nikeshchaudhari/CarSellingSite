from turtle import pos
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from sklearn.decomposition import TruncatedSVD
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json


# Create your views here.

@login_required
def my_favourate_ad(request):
    obj = Favourate.objects.filter(user = request.user,favourate=True)
    context = {'obj': obj}
    return render(request,'my-favourate.html',context)

@csrf_exempt
def add_to_favourate(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        car = Owner_Detail.objects.get(id=pk)
        is_fav = False
        if car:
            try:
                fav_obj_exist = Favourate.objects.filter(user=request.user, car_detail = car).exists()
                if fav_obj_exist:
                    fav_obj = Favourate.objects.get(user=request.user, car_detail = car)
                    if fav_obj.favourate:
                        fav_obj.favourate = False
                    else:
                        fav_obj.favourate = True
                        is_fav = True
                else:
                    fav_obj = Favourate.objects.create(user=request.user, car_detail = car)
                    fav_obj.favourate = True
                    is_fav = True

                
                fav_obj.save()
            except Exception as e:
                print(e)
        return JsonResponse({'is_fav': is_fav})

def home(request):
    return render(request,'carousel.html')
def About(request):
    return render(request,'about.html')

def signup(request):
    error = ""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        u=request.POST['uname']
        p=request.POST['pwd']
        ad=request.POST['add']
        m=request.POST['mobile']
        g=request.POST['male']
        d=request.POST['birth']
        e=request.POST['email']
        i=request.FILES['img']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=u,password=p,email=e)
            Register.objects.create(user=user,gen=g,add=ad,mobile=m,birth=d,image=i)
            error = "no"
        except:
            error = "yes"
    d={'error':error}
    return render(request,'signup.html',d)

def signin(request):
    error = ""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            elif user:
                login(request, user)
                error = "no"
        except:
            error = "yes"
    d={'error':error}
    return render(request,'signin.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Search(request):
    room=Status.objects.filter(status = True)
    state1=State.objects.all()
    if request.method=='POST':
        s=request.POST['state']
        state=State.objects.filter(state=s).first()
        return redirect('dist',state.id)
    d = {'state': state1,'room':room}
    return render(request,'serach.html',d)

def dist(request,dist):
    state=State.objects.get(id=dist)
    room=Owner_Detail.objects.filter(state=state).all()
    dist=District.objects.filter(state=dist)
    if request.method=='POST':
        s=request.POST['dist']
        dist1=District.objects.filter(dist=s).first()
        return redirect('room',dist1.id)
    d={'dist':dist,'state':state,'room':room}
    return render(request,'dist.html',d)

def room(request,dist):
    dist1 = District.objects.get(id=dist)
    room = Owner_Detail.objects.filter(dist=dist1)
    d={'room':room,'dist':dist1}
    return render(request,'room.html',d)

def detail(request,id):
    own=Owner_Detail.objects.get(id=id)
    img = Image.objects.filter(owner=own)
    d={'img':img,'dist':own}
    return render(request,'detail.html',d)

def detail1(request,dist):
    if not request.user.is_authenticated:
        return redirect('home')
    own=Owner_Detail.objects.get(id=dist)
    img = Image.objects.filter(owner=own)
    d={'img':img,'dist':own}
    return render(request,'detail1.html',d)


def Contact(request):
    return render(request,'contact.html')

def rent1(request):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    st=State.objects.all()
    if request.method=="POST":
        try:
            s=request.POST['state']
            state=State.objects.filter(state=s).first()
            return redirect('rent',state.id)

        except:
            pass

    d={'state':st,'error':error}
    return render(request,'rent.html',d)

def rent(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    st2=State.objects.all()
    st=State.objects.get(id=pid)
    dist2=District.objects.filter(state=st)
    if request.method=="POST":
        try:
            s=request.POST['state']
        except:
            pass
        try:
            d=request.POST['dist']
            l=request.POST['local']
            t=request.POST['title']
            de=request.POST['desc']
            p=request.POST['price']
            i=request.FILES['img']
            b = request.POST['brand']
            m = request.POST['model']
            y = request.POST['year']
            f = request.POST['fuel']
            k = request.POST['kmdriven']
            n = request.POST['noofowner']
            dist1=District.objects.filter(dist=d).first()
            req=User.objects.filter(username=request.user.username).first()
            re=Register.objects.filter(user=req).first()
            # status=Status.objects.get(status="pending")
            add_car = Owner_Detail.objects.create(register=re,state=st,dist=dist1,title=t,local_add=l,desc=de,price=p,img=i,brand=b,model=m,year=y,fuel=f,kmdriven=k,noofowner=n)
            Status.objects.create(car = add_car,status = False)
            add_car.save()
            error=True
        except:
            pass
    d={'dist':dist2,'state':st2,'st':st,'error':error}
    return render(request,'rent.html',d)

def Room_Img(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user=User.objects.get(id=request.user.id)
    reg=Register.objects.filter(user=user).first()
    room=Owner_Detail.objects.filter(register=reg).all()
    d={'room':room}
    return render(request,'room_image.html',d)

def Add_Room_Img(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    room=Owner_Detail.objects.get(id=pid)
    if request.method=="POST":
        r=request.POST['name']
        i=request.FILES['img']
        Image.objects.create(owner=room,room_name=r,img=i)
        error=True
    d={'error':error,'pid':pid}
    return render(request,'add_room_img.html',d)

def Owner_detail(request,pid):
    own=Owner_Detail.objects.get(id=pid)
    d={'own':own}
    return render(request,'owner_detail.html',d)

def User_detail(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user=User.objects.filter(id=request.user.id).first()
    register=Register.objects.filter(user=user).first()
    d={'register':register}
    return render(request,'user_detail.html',d)


def edit_detail(request,data):
    if not request.user.is_authenticated:
        return redirect('home')
    error = False
    st = State.objects.all()
    if request.method == "POST":
        try:
            s = request.POST['state']
            state = State.objects.filter(state=s).first()
            return redirect('edit_detail', state.id,data)

        except:
            pass

    d = {'state': st, 'error': error}
    return render(request, 'edit_detail.html', d)


def Edit_detail(request,sid,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    data=Owner_Detail.objects.get(id=pid)
    state=State.objects.all()
    st = State.objects.get(id=sid)
    dist2 = District.objects.filter(state=st)
    if request.method=="POST":
        try:
            s = request.POST['state']
        except:
            pass
        d = request.POST['dist']
        l = request.POST['local']
        t = request.POST['title']
        de = request.POST['desc']
        p = request.POST['price']
        b = request.POST['brand']
        m = request.POST['model']
        y = request.POST['year']
        f = request.POST['fuel']
        k = request.POST['kmdriven']
        n = request.POST['noofowner']

        try:
            i = request.FILES['img']
            data.img = i
            data.save()
        except:
            pass

        dist1 = District.objects.filter(dist=d).first()
        data.state = st
        data.dist = dist1
        data.desc = de
        data.price = p
        data.local_add = l
        data.title = t
        data.brand = b
        data.model = m
        data.year = y
        data.fuel = f
        data.kmdriven = k
        data.noofowner = n
        data.save()
        error=True
    d={'data':data,'dist':dist2,'state':state,'st':st,'error':error}
    return render(request,'edit_detail.html',d)

def delete_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=Owner_Detail.objects.get(id=pid)
    Own.delete()
    return redirect('my_car_list')


def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(id=pid)
    user.delete()
    #Own=Register.objects.get(id=pid)
    #Own.delete()
    return redirect('view_user')

def delete_dist(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=District.objects.get(id=pid)
    Own.delete()
    return redirect('view_dist')

def delete_state(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=State.objects.get(id=pid)
    Own.delete()
    return redirect('view_state')

def View_User(request):
    if not request.user.is_staff:
        return redirect('home')
    data=Register.objects.all()
    d={'data':data}
    return render(request,'view_user.html',d)

def Edit_User(request,pid):
    if not request.user.is_staff:
        return redirect('home')
    error = False
    data=Register.objects.get(id=pid)
    if request.method=="POST":
        u=request.POST['uname']
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        m=request.POST['mobile']
        a=request.POST['add']
        data.user.username=u
        data.user.first_name=f
        data.user.last_name=l
        data.user.email=e
        data.add=a
        data.mobile=m
        data.save()
        error=True
    d={'data':data,'error':error}
    return render(request,'edit_user.html',d)

def Edit_State(request,pid):
    if not request.user.is_staff:
        return redirect('home')
    error = False
    data=State.objects.get(id=pid)
    if request.method=="POST":
        u=request.POST['state']
        data.state=u
        data.save()
        error=True
    d={'data':data,'error':error}
    return render(request,'edit_state.html',d)

def Add_State(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method=="POST":
        s=request.POST['state']
        State.objects.create(state=s)
        return redirect('view_state')
    return render(request,'add_state.html')

def Add_District(request):
    if not request.user.is_staff:
        return redirect('home')
    state=State.objects.all()
    if request.method=="POST":
        s=request.POST['state']
        d=request.POST['dist']
        st=State.objects.get(state=s)
        District.objects.create(state=st,dist=d)
        return redirect('view_dist')
    d={'state':state}
    return render(request,'add_dist.html',d)

def View_State(request):
    if not request.user.is_staff:
        return redirect('home')
    state=State.objects.all()
    d={'state':state}
    return render(request,'view_state.html',d)

def View_District(request):
    if not request.user.is_staff:
        return redirect('home')
    dist=District.objects.all()
    d={'dist':dist}
    return render(request,'view_dist.html',d)

def View_Request(request):
    if not request.user.is_staff:
        return redirect('home')
    error=True
    car_list = Status.objects.filter(status=False)
    d={'car_list':car_list}
    return render(request,"request.html",d)

def Change(request,id):
    if not request.user.is_staff:
        return redirect('home')
    status  = Status.objects.get(id=id)
    if status:
        if status.status:
            return redirect('request')
        status.status = True
        status.save()
    return redirect('request')

def All_Ads(request):
    if not request.user.is_staff:
        return redirect('home')
    data=Owner_Detail.objects.all()
    d={'data':data}
    return render(request,'all_ads.html',d)

def Change_Img(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=""
    img=Image.objects.get(id=pid)
    if request.method=="POST":
        try:
            i=request.FILES['img']
            n=request.POST['name']
            img.room_name=n
            img.img=i
            img.save()
            error="no"
        except:
            error="yes"
    d={'error':error,'img':img}
    return render(request,'changeimg.html',d)

def Feedback(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        Send_Feedback.objects.create( message1=m, email=e,contact=con)
    return render(request, 'feedback.html')

def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)  




