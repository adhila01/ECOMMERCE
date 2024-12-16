from django.shortcuts import render
from django.shortcuts import render,redirect


from django.http import HttpResponse
from django.conf import settings
# import stripe
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from .models import UserRegister
from .models import *


# Create your views here.


def index(request):
    return render(request,'index.html')


def reg(request):
    if (request.method=='POST'):
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        propic=request.FILES.get('propic')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if(password==cpassword):
            data=UserRegister(fullname=fullname,email=email,phone=phone,propic=propic,gender=gender,password=password)
            data.save()
            return HttpResponse("registration success")
        else:
            return HttpResponse("registration failed")
    return render(request,'registration.html')

def userlogin(request):
    if(request.method=='POST'):
        email=request.POST.get('email')
        password=request.POST.get('password')
        data=UserRegister.objects.all()
        for i in data:
            if(i.email==email and i.password==password):
                request.session['userid']=i.id
                return redirect(userprofile)
        else:
            return HttpResponse("login failed")
    return render(request,'userlogin.html')

def logout(request):
    request.session.flush()
    return redirect(index)


def userprofile(request):
    try:
      category=request.GET.get('category','all')#get selecetd category,if there is no category all option  will work
      id1=request.session['userid']  #session calling
      data=UserRegister.objects.get(id=id1)
      if category == 'all':
        db=SellerProductUpload.objects.all()
      else:
        db=SellerProductUpload.objects.filter(category=category)
    # pre-process the size data
      for item in db:
         item.sizes = item.sizes.split(',')
      return render (request, 'userprofile.html',{'data':data,'db':db })
    except KeyError:
        return redirect(userlogin)


def usersingleview(request):
    id1 = request.session['userid']
    data=UserRegister.objects.get(id=id1)
    return render(request,'usersingleview.html',{'data':data})

def updateuserdetails(request):
    id1 = request.session['userid']
    data = UserRegister.objects.get(id=id1)
    if (request.method == 'POST'):
        if (request.FILES.get('propic') == None):
            data.save()
        else:
            data.propic.request.FILES.get('propic')
            data.fullname = request.POST.get('fullname')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.gender = request.POST.get('gender')
        data.save()
        return redirect(userprofile)

    return render(request, 'updateuserdetails.html', {'data': data})

def productupload(request):
    if(request.method=='POST'):
        productname=request.POST.get('product')
        price=request.POST.get('price')
        proimg=request.FILES.get('productimg')
        sizes=request.POST.get('size')
        desc=request.POST.get('description')
        category=request.POST.get('category')
        data=SellerProductUpload(productname=productname,price=price,proimg=proimg,sizes=sizes,desc=desc,category=category)
        data.save()
        return HttpResponse('item added')
    else:

        return render(request,'sellerproductupload.html')

def addtocart(request,itemid):
    item=SellerProductUpload.objects.get(id=itemid) #to fetch the details of item with particular id
    cart=CartItem.objects.all()
    size=''
    if(request.method=='GET'):
        size=request.GET.get('size')

    for i in cart:
        if i.item.id==itemid and i.selectedsize==size and i.userid==request.session['userid']:
            i.quantity+=1
            i.save()
            return redirect(Cartdisplay)
    else:

            db=CartItem(userid=request.session['userid'],item=item,selectedsize=size)
            db.save()
            return redirect(Cartdisplay)

def Cartdisplay(request):
    userid=request.session['userid']
    db=CartItem.objects.filter(userid=userid)
    total=0
    count=0
    for i in db:
        i.item.price*=i.quantity
        total +=i.item.price
        count+=1
    return render(request,'cartdisplay.html',{'db':db,'total':total,'count':count})

def inc_dec(request,itemid):
    db=CartItem.objects.get(id=itemid)
    action=request.GET.get('action')
    if action=='increment':
        db.quantity+=1
        db.save()
    elif action=='decrement' and db.quantity>0:
        db.quantity-=1
        db.save()

    return redirect(Cartdisplay)

def deletecart(request,cartid):
    db=CartItem.objects.get(id=cartid)
    action=request.GET.get('action')
    if(action=='remove'):
        db.delete()
    return redirect(Cartdisplay)



def wishlistdisplay(request):
    userid=request.session['userid']
    db = wishlist.objects.filter(userid=userid)
    for i in db:
        i.item.sizes=i.item.sizes.split(',')
    return render(request,'wishlist.html',{'db':db})

def wishli(request,cartid):
    item=SellerProductUpload.objects.get(id=cartid)
    wish=wishlist.objects.all()
    for i in wish:
        if i.item.id==cartid and i.userid==request.session['userid']:
            return redirect(wishlistdisplay)
    else:
            db = wishlist(userid=request.session['userid'], item=item)
            db.save()

            return redirect(wishlistdisplay)


def wishlistdelete(request,wishliid):
    db=wishlist.objects.get(id=wishliid)
    db.delete()
    return redirect(wishlistdisplay)

def addaddress(request):
    id1= request.session['userid']
    userdata=UserRegister.objects.get(id=id1)
    if(request.method=='POST'):
        addressline1=request.POST.get('address1')
        addressline2=request.POST.get('address2')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        contactname=request.POST.get('contact_name')
        contactnumber=request.POST.get('contact_number')
        db=Addressdetails(userdetails=userdata,address_line1=addressline1,address_line2=addressline2,pincode=pincode,city=city,state=state,contact_name=contactname,contact_number=contactnumber)
        db.save()
        return redirect(delivery_details)
    else:
        return render(request,'add address.html')

def  delivery_details(request):
    userid=request.session['userid']
    data=Addressdetails.objects.filter(userdetails__id=userid)
    return render(request,'delivery address.html',{'data':data})

def summary(request):
    userid=request.session['userid']
    address_id=request.GET.get('address')
    print(address_id)
    address=Addressdetails.objects.get(id=address_id)
    cartitems =CartItem.objects.filter(userid=userid)
    key=settings.STRIPE_PUBLISHABLE_KEY
    total=0
    stripetotal=0
    for i in cartitems:
        total+=i.item.price
        stripetotal=total*100
    return render(request,'summary.html', {'address': address, 'cartitem': cartitems,'total':total,'key':key,'stripetotal':stripetotal})



def create_order(request): #after payment
    if request.method == 'POST':
        order_items = []
        total_price = 0
        userid = request.session['userid'] #user id session calling
        user = UserRegister.objects.get(id=userid) #registered details
        address_id = request.POST.get('address_id')#hidden filed address id
        print("address id=",address_id)
        address = Addressdetails.objects.get(id=address_id)#fetch address using the address id
        cart = CartItem.objects.filter(userid=userid)#cart filter
        #create the order objects
        order=Order.objects.create(userdetails=user,address=address)#automatically save
        for i in cart:
            #create order item for each cart item
            OrderItems.objects.create(   #modelekk olla data
                order=order,
                order_pic=i.item.proimg,
                pro_name=i.item.productname,
                quantity=i.quantity,
                price=i.item.price
            )

            total_price += i.item.price*i.quantity
            order_items.append({   #mailekk olla data
                'product': i.item.productname,
                'quantity': i.quantity,
                'price': i.item.price *i.quantity,

            })
        expected_delivery_date = datetime.now()+timedelta(days=7) #expected delivery date

        #construct email content
        subject='order confirmation'

        context = {
            'order_items': order_items, #list of items
            'total_price': total_price, #total price
            'expected_delivery_date': expected_delivery_date.strftime('%y-%m-%d')
        }

        html_message = render_to_string('order_confirmation_email.html', context) # to return string
        plain_message = strip_tags(html_message)
        from_email = 'adhila9539@gmail.com'
        to_email = [user.email]

        #send mail

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        cart.delete()
        return HttpResponse('order created successfully')


def order_view(request):
    userid = request.session['userid']
    order = OrderItems.objects.filter(order__userdetails__id=userid).order_by('-order__ordered_date')
    return render(request, 'order.html', {'order': order})

def order_cancel(request,id):
    userid=request.session['userid']
    user = UserRegister.objects.get(id=userid)
    db=OrderItems.objects.get(id=id)
    db.order_status=False
    db.save()
    subject = 'order cancelled'
    context = {
        'product_name': db.pro_name,
        'price':db.price
    }
    html_message=render_to_string('order_cancellation.html',context)
    plain_message=strip_tags(html_message)
    from_email='adhila9539@gmail.com'
    to_email=[user.email]
    send_mail(subject,plain_message,from_email,to_email,html_message=html_message)

    #email sending
    return HttpResponse('order cancelled')

def changepassword(request):
    id1=request.session['userid']
    db=UserRegister.objects.get(id=id1)
    if(request.method=='POST'):
        oldpassword=request.POST.get('old')
        if db.password == oldpassword:
            newpassword=request.POST.get('new')
            retypepassword=request.POST.get('retype')
            if(newpassword==retypepassword):
                db.password=newpassword
                db.save()
                return redirect(userlogin)
            else:
                messages.error(request,'password dont match')
        else:
            messages.error(request,'please enter correct password')
    return render(request,'passwordchange.html')



# Create your views here.
