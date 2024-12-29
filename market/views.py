from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout,get_user_model,update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .models import CustomUser,Restaurant,Motel,OrderFood,OrderDrinks,OrderRoom
from django.contrib import messages
from django.db import transaction
from .forms import (LoginForm,RegisterForm,EditForm,DishesForm,
	RoomsForm,DishesForm,ChangeUserForm)     

# Create your views here.

#CustomUser=get_user_model()

class CustomPasswordChangeView(PasswordChangeView):
    form_class=ChangeUserForm
    template_name="pasguru.html"
    success_url=reverse_lazy('password_change_done')
    
    
@login_required
def changed_password(request):
    return render(request,"success_page.html")



@login_required
def change_password(request):
    messages=""
    if request.method=="POST":
        form=ChangeUserForm(request.POST)
        if form.is_valid():
            cpwd=form.cleaned_data['currentpassword']
            pass1=form.cleaned_data['newpassword']
            pass2=form.cleaned_data['repeatpassword']
            
            if pass1!=pass2 and request.user.check_password(cpwd)!=True:
                messages="Passwords don't match!!"
            else:
                user=authenticate(username=request.user.username,password=pass2)
                if user is not None:
                    user.set_password(pass2)
                    update_session_auth_hash(request,user)
                    login(request,user)
                    messages="Password Successfully Updated!!"
                    return redirect('success_page')
                else:
                    messages="Invalid Current Password!!"
                
    else:
        form=ChangeUserForm()
    return render(request,'pasguru.html',{'form':form,'messages':messages})

def creation_success(request):
    return render(request,"registration_success.html")

def creation_failure(request):
    return render(request,"registration_error.html")

@login_required
def room_service_success(request):
    return render(request,"book_room_success.html")

@login_required
def room_unavailable(request):
    return render(request,"try_another_room.html")

@login_required
def food_service_success(request):
    return render(request,"dish_success.html")

@login_required
def edit_success(request):
    return render(request,"edit_user_succ.html")

@login_required
def room_service(request):
    if request.method=='POST':
        form=RoomsForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            pic=form.cleaned_data['photo']
            cid=form.cleaned_data['check_in_date']
            cod=form.cleaned_data['check_out_date']
            
            price=form.cleaned_data['price'].replace('Kes','')
            float_price=float(price)
            
            duration=(cod-cid).days
            total=duration*int(price)
        
            if Motel.objects.filter(room_id=name,is_booked=True).exists():
                return redirect('try_another')
            elif Motel.objects.filter(user=user).exists():
                return redirect("home")
            else:
                try:
                    with transaction.atomic():
                        room=Motel.objects.create(user=user,room_id=name,room_photo=pic,room_cid=cid,room_cod=cod,room_price=price,room_bill=total,is_booked=True)
                        OrderRoom.objects.create(user=user,room=room,room_price=float_price,check_in_date=cid,check_out_date=cod)
                        return redirect("book_room_success")
                except Exception as e:
                    print(f"Caught:{str(e)}")    
    else: 
        form=RoomsForm()
    return render(request,"accomodation.html",{'form':form})


@login_required
def food_service(request):
    if request.method=="POST":
        form=DishesForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            pic=form.cleaned_data['photo']
            qty=form.cleaned_data['quantity']
            price=form.cleaned_data['price'].replace("Kes ","")
            total=form.cleaned_data['total'].replace("Kes ","")                
            try:
                with transaction.atomic():
                    food=Restaurant.objects.create(user=user,food_id=name,food_photo=pic,food_quantity=qty,food_price=price,food_bill=total)
                    OrderFood.objects.create(user=user,food=food,quantity=qty,bill=float(qty*price))
                    return redirect("dish_success")
            except Exception as e:
                transaction.rollback()
                return HttpResponse(f"Error:{str(e)}")
    else:
        form=DishesForm()
    foods=Restaurant.objects.all()
    return render(request,"dishes.html",{'form':form})

@login_required
def check_out(request):
    order=OrderRoom.objects.get(id=request.user.id)
    
    #update Motel instance
    room=order.room_id
    room.is_booked=False
    room.room_cid=None
    room.room_cod=None
    room.save()
    return redirect("checkout_success")

@login_required
@transaction.atomic
def customer_page(request):
    myfoods=Restaurant.objects.filter(user=request.user)
    myrooms=Motel.objects.filter(user=request.user)
    return render(request,'home.html',{'myfoods':myfoods,'myrooms':myrooms})

@login_required
@transaction.atomic
def supervisor_page(request):
    records=CustomUser.objects.filter(is_superuser=False)
    order_food=OrderFood.objects.all()
    order_room=OrderRoom.objects.all()
    mydict={'records':records,'orderF':order_food,'orderR':order_room}
    return render(request,'dash.html',context=mydict)
    
@login_required
def AddUser(request):
    mydict={}
    form=EditForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('origin')
    mydict['form']=form
    return render(request,'add.html',mydict)

@login_required
def EditUser(request,id=None):
    if request.method=='POST':
        form=EditForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            fname=form.cleaned_data['firstname']
            lname=form.cleaned_data['lastname']
            uname=form.cleaned_data['username']
            mail=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone']
            
            user=CustomUser.objects.filter(email=mail)
            if user.exists():
                user.username=uname
                user.first_name=fname
                user.last_name=lname
                user.phone=phone_no
                return redirect('lounge')
    else:
        form=EditForm()
    return render(request,'dash.html',{'form':form})

@login_required
def DeleteUser(request,eid=None):
    one_rec=CustomUser.objects.get(pk=eid)
    if request.method=="POST":
        one_rec.delete()
        return redirect('origin')
    return render(request,'delete.html')

@login_required
def ViewUser(request,eid=None):
    mydict={}
    one_rec=CustomUser.objects.get(pk=eid)
    mydict['user']=one_rec
    return render(request,'dash.html',mydict)

def user_logout(request):
    logout(request)
    return redirect('login')


def signin(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            
            user=authenticate(username=username,password=password)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    #messages.success(request,"Login Successfully!!")
                    return redirect("dash")#'dashboard')#admins page
                else:
                    #messages.success(request,'Congrats for successful login!!')
                    return redirect("home")
            else:
                messages.error(request,"Invalid username or password")
    else:
        form=LoginForm()
    return render(request,"login.html",{'form':form})

def signup(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            email=form.cleaned_data['email']
            firstname=form.cleaned_data['firstname']
            lastname=form.cleaned_data['lastname']
            phone=form.cleaned_data['phone']
            password=form.cleaned_data['password']
            
            if CustomUser.objects.filter(email=email).exists():
                return redirect("signup-error")
            else:
                CustomUser.objects.create_user(username=uname,first_name=firstname,
                                               last_name=lastname,email=email,phone=phone,password=password)
                return redirect("signup-complete")#login is the template
    else:
        form=RegisterForm()
    return render(request,"register.html",{'form':form})


def mirror(request):
    return render(request,"origin.html")