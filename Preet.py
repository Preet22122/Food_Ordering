from datetime import date
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from myconnection import *
import http.client
import time
def openadminlogin(request):
    return render(request,'adminlogin.html')
def checkadminlogin(request):
    email=request.GET['email']
    password=request.GET['password']
    conn=myconnection.connect('')
    cr=conn.cursor()
    query="select * from admin where email='"+email+"' and password='"+password+"'"
    cr.execute(query)
    result=cr.fetchone()
    if result==None:
        return render(request,'adminlogin.html',{"message":'invalid email/password'})
    else:
        request.session['adminemail']=email
        return render(request,'admindashboard.html')
def admindashboard(request):
    if request.session.has_key('adminemail'):
        return render(request, 'admindashboard.html')
    else:
        return render(request, 'adminlogin.html')
def openadminchangepass(request):
    if request.session.has_key('adminemail'):
        return render(request,'adminchangepassword.html')
    else:
        return render(request, 'adminlogin.html')
def changeadminpassword(request):
    if request.session.has_key('adminemail'):
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        conn = myconnection.connect('')
        cr = conn.cursor()
        email=""
        if request.session.has_key('adminemail'):
            email = request.session['adminemail']
            query = "select * from admin where email='" + email + "' and password='" + oldpass + "'"
            cr.execute(query)
            result = cr.fetchone()
            if result == None:
                return render(request, 'adminchangepassword.html', {"message": 'old password not match!!'})
            else:
                query = "update admin set password='" + newpass + "' where email='" + email + "'"
                cr.execute(query)
                conn.commit()
                return render(request, 'adminchangepassword.html', {"message": 'password changed successfully!!'})
        else:
            return HttpResponseRedirect('openadminlogin')
    else:
        return render(request, 'adminlogin.html')
def adminlogout(request):
    del request.session['adminemail']
    return HttpResponseRedirect('adminlogin')
def openaddproducts(request):
    if request.session.has_key('adminemail'):
        list=myconnection.fethcategories('')
        return render(request,'addproducts.html',{"list":list})
    else:
        return render(request, 'adminlogin.html')
@csrf_exempt
def addproduct(request):
    if request.session.has_key('adminemail'):
        print()
        cname = request.POST['cname']
        pname=request.POST['pname']
        decription = request.POST['description']
        sp = request.POST['sellingprice']
        cp= request.POST['costprice']
        discount = request.POST['discount']
        quantity= request.POST['quantity']
        fs=FileSystemStorage()
        photo=request.FILES['photo']
        fs.save("products/"+photo.name,photo)
        conn=myconnection.connect('')
        cr=conn.cursor()
        query="insert into products values(NULL,'"+pname+"','"+decription+"','"+str(cp)+"','"+str(sp)+"','"+str(discount)+"','"+str(photo.name)+"','"+str(quantity)+"','"+str(cname)+"')"
        cr.execute(query)
        conn.commit()
        return HttpResponse('success')
    else:
        return render(request, 'adminlogin.html')
def openviewproducts(request):
    if request.session.has_key('adminemail'):
        return render(request,'viewproducts.html')
    else:
        return render(request, 'adminlogin.html')
def viewproducts(request):
    if request.session.has_key('adminemail'):
        conn=myconnection.connect('')
        cr=conn.cursor()
        query="select * from products"
        cr.execute(query)
        result=cr.fetchall()
        list=[]
        for row in result:
            list.append(row)
        return JsonResponse(list,safe=False)
    else:
        return render(request, 'adminlogin.html')
def deleteproduct(request):
    if request.session.has_key('adminemail'):
        pid=request.GET['pid']
        conn = myconnection.connect('')
        cr = conn.cursor()
        query = "delete  from products where pid='"+str(pid)+"'"
        cr.execute(query)
        conn.commit()
        return HttpResponse('success')
    else:
        return render(request, 'adminlogin.html')
def gotoeditproductpage(request):
    if request.session.has_key('adminemail'):
        pid = request.GET['pid']
        conn = myconnection.connect('')
        cr = conn.cursor()
        query="select * from products where pid='"+str(pid)+"'"
        cr.execute(query)
        row=cr.fetchone()
        d = {}
        d['pid'] = pid
        d['pname'] = row[1]
        d['description'] = row[2]
        d['cp'] = row[3]
        d['sp'] = row[4]
        d['discount'] = row[5]
        d['photo'] = row[6]
        d['quantity'] = row[7]
        d['cname'] = row[8]
        x = myconnection.fethcategories('')
        list=[]
        list.append(x)
        list.append(d)
        return render(request,'editproduct.html',{"data":list})
    else:
        return render(request, 'adminlogin.html')
@csrf_exempt
def editproduct(request):
    if request.session.has_key('adminemail'):
        print()
        cname = request.POST['cname']
        pid= request.POST['pid']
        pname=request.POST['pname']
        decription = request.POST['description']
        sp = request.POST['sellingprice']
        cp= request.POST['costprice']
        discount = request.POST['discount']
        quantity= request.POST['quantity']
        hidden =request.POST['hidden']
        query=""
        fs = FileSystemStorage()
        if hidden=="nofile":
            query = "update products set pname='" + pname + "',description='" + decription + "',cp='" + str(cp) + "',sp='" + str(sp) + "',discount='" + str(discount) + "',quantity='" + str(quantity) + "',cname='" + str(cname) + "' where pid='" + str(pid) + "'"
        else:
            photo = request.FILES['photo']
            fs.save("products/" + photo.name, photo)
            query = "update products set pname='" + pname + "',description='" + decription + "',cp='" + str(cp) + "',sp='" + str(sp) + "',discount='" + str(discount) + "',quantity='" + str(quantity) + "',photo='"+photo.name+"',cname='" + str(cname) + "' where pid='" + str(pid) + "'"
        conn=myconnection.connect('')
        cr=conn.cursor()
        cr.execute(query)
        conn.commit()
        return HttpResponse('success')
    else:
        return render(request, 'adminlogin.html')
def manageproductphotos(request):
    if request.session.has_key('adminemail'):
        pid=request.GET['pid']
        conn = myconnection.connect('')
        cr=conn.cursor()
        query="select * from photos where pid='"+str(pid)+"'"
        cr.execute(query)
        result=cr.fetchall()
        x=[]
        for row in result:
            d={}
            d['photoid']=row[0]
            d['pid'] = row[1]
            d['photopath'] = row[2]
            d['type'] = row[3]
            x.append(d)
        list=[]
        list.append(x)
        list.append(pid)
        return render(request,'manageproductphotos.html',{"data":list})
    else:
        return render(request, 'adminlogin.html')
@csrf_exempt
def insertphoto(request):
    if request.session.has_key('adminemail'):
        pid= request.POST['pid']
        type=request.POST['type']
        fs=FileSystemStorage()
        photo=request.FILES['photo']
        fs.save("products/"+photo.name,photo)
        conn=myconnection.connect('')
        cr=conn.cursor()
        query="insert into photos values(NULL,'"+str(pid)+"','"+str(photo.name)+"','"+str(type)+"')"
        cr.execute(query)
        conn.commit()
        return HttpResponseRedirect('manageproductphotos?pid='+pid)
    else:
        return render(request, 'adminlogin.html')
def deleteproductphoto(request):
    if request.session.has_key('adminemail'):
        photoid=request.GET['photoid']
        pid=request.GET['pid']
        conn = myconnection.connect('')
        cr = conn.cursor()
        query = "delete  from photos where photoid='" + str(photoid) + "'"
        cr.execute(query)
        conn.commit()
        return HttpResponseRedirect('manageproductphotos?pid=' + pid)
    else:
        return render(request, 'adminlogin.html')
def openuserdashboard(request):
    request.session['page'] = 'userdashboard'
    return render(request,'userdashboard.html')
def insertcart(request):
    if request.session.has_key('cart'):
        username = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        mobile = request.POST['mobile']
        totalbill = request.POST['totalbill']
        print(username, address, mobile, email, totalbill)
        conn = myconnection.connect('')
        cr = conn.cursor()
        td = date.today()
        print('td ', td)
        query1 = "insert into myorder values(NULL,'" + username + "','" + address + "','" + email + "','" + str(
            totalbill) + "','" + str(mobile) + "','" + str(td) + "')"
        print('my q', query1)
        cr.execute(query1)
        conn.commit()
        s = "select * from myorder"
        cr.execute(s)
        rs = cr.fetchall()
        orderid = ""
        msg = "order placed successfully total bill Rs " + str(totalbill)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=monika&password=L78E7CIB&message=" + msg + "&phone_numbers=" +
                      request.POST["mobile"])
        response = conn1.getresponse()
        print(response.read())
        for row in rs:
            orderid = row[0]
        x = request.session['cart']
        for item in x:
            query2 = "insert into orderdetail values(NULL,'" + str(orderid) + "','" + str(item['pid']) + "','" + str(
                item['pname']) + "','" + str(item['quantity']) + "','" + str(item['sp']) + "','" + str(
                item['discount']) + "','" + str(item['netprice']) + "','" + str(item['totalprice']) + "')"
            cr.execute(query2)
            conn.commit()
        del request.session['cart']
        del request.session['cartsize']
        list = []
        list.append(x)
        list.append(totalbill)
        list.append(address)
        list.append(mobile)
        list.append(username)
        return render(request, 'payment successfull.html', {"data": list})
    else:
        return HttpResponseRedirect('openuserdashboard')

def viewfilteredproducts(request):
    conn=myconnection.connect('')
    cr=conn.cursor()
    value=request.GET['value']
    query="select * from products where pname LIKE '"+value+"%'"
    cr.execute(query)
    result=cr.fetchall()
    list=[]
    for row in result:
        list.append(row)
    return JsonResponse(list,safe=False)
def addtocart(request):
    current_milli_time = int(round(time.time() * 1000))
    pid=request.GET['pid']
    quantity= request.GET['quantity']
    print(quantity," ",pid)
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from products where pid='" + str(pid) + "'"
    cr.execute(query)
    row = cr.fetchone()
    d = {}
    d['pid'] = pid
    d['pname'] = row[1]
    d['description'] = row[2]
    d['cp'] = row[3]
    d['sp'] = row[4]
    d['discount'] = row[5]
    d['photo'] = row[6]
    d['quantity'] = row[7]
    d['cname'] = row[8]
    netprice=(float)( row[4])-(float)( row[5])
    totalprice=netprice*(int)(quantity)
    d['netprice']=netprice
    d['quantity']=quantity
    d['totalprice'] = totalprice
    d['ct']=current_milli_time
    if request.session.has_key('cart'):
        list=request.session['cart']
        list.append(d)
        request.session['cart']=list
        request.session['cartsize']=len(list)
    else:
        list = []
        list.append(d)
        request.session['cart'] = list
        request.session['cartsize'] = len(list)
    return HttpResponse('success')
def deleteitemfromcart(request):
    pid=request.GET['pid']
    ct = request.GET['ct']
    list = request.session['cart']
    newlist=[]
    for row in list:
        print(row['ct']," ",ct)
        if row['pid']==pid and str(row['ct'])==str(ct):
            print()
        else:
            newlist.append(row)
    request.session['cart'] = newlist
    request.session['cartsize'] = len(newlist)
    if len(newlist)==0:
        del request.session['cart']
        del request.session['cartsize']
    return HttpResponseRedirect('viewcart')
def viewcart(request):
    if request.session.has_key('cart'):
        x = request.session['cart']
        totalcartbill=0
        for item in x:
            totalcartbill=totalcartbill+(float)(item['totalprice'])
        list=[]
        list.append(x)
        list.append(totalcartbill)
        list.append(totalcartbill*100)
        request.session['page']='viewcart'
        return render(request,'viewcart.html',{"data":list})
    else:
        return HttpResponseRedirect('openuserdashboard')
def productdetailpage(request):
    pid = request.GET['pid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from photos where pid='" + str(pid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    for row in result:
        d = {}
        d['photoid'] = row[0]
        d['pid'] = row[1]
        d['photopath'] = row[2]
        d['type'] = row[3]
        x.append(d)
    list = []
    list.append(x)
    query = "select * from products where pid='" + str(pid) + "'"
    cr.execute(query)
    row = cr.fetchone()
    d = {}
    d['pid'] = pid
    d['pname'] = row[1]
    d['description'] = row[2]
    print(row[2])
    d['cp'] = row[3]
    d['sp'] = row[4]
    d['discount'] = row[5]
    d['photo'] = row[6]
    d['quantity'] = row[7]
    d['cname'] = row[8]
    list.append(d)
    return  render(request,'productdetail.html',{"data":list})
def insertcart(request):
    if request.session.has_key('cart'):
        username = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        mobile = request.POST['mobile']
        totalbill = request.POST['totalbill']
        print(username, address, mobile, email, totalbill)
        conn = myconnection.connect('')
        cr = conn.cursor()
        td = date.today()
        print('td ', td)
        query1 = "insert into myorder values(NULL,'" + username + "','" + address + "','" + email + "','" + str(
            totalbill) + "','" + str(mobile) + "','" + str(td) + "')"
        print('my q', query1)
        cr.execute(query1)
        conn.commit()
        s = "select * from myorder"
        cr.execute(s)
        rs = cr.fetchall()
        orderid = ""
        msg = "order placed successfully total bill Rs " + str(totalbill)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=monika&password=L78E7CIB&message=" + msg + "&phone_numbers=" +
                      request.POST["mobile"])
        response = conn1.getresponse()
        print(response.read())
        for row in rs:
            orderid = row[0]
        x = request.session['cart']
        for item in x:
            query2 = "insert into orderdetail values(NULL,'" + str(orderid) + "','" + str(item['pid']) + "','" + str(
                item['pname']) + "','" + str(item['quantity']) + "','" + str(item['sp']) + "','" + str(
                item['discount']) + "','" + str(item['netprice']) + "','" + str(item['totalprice']) + "')"
            cr.execute(query2)
            conn.commit()
        del request.session['cart']
        del request.session['cartsize']
        list = []
        list.append(x)
        list.append(totalbill)
        list.append(address)
        list.append(mobile)
        list.append(username)
        return render(request, 'payment successfull.html', {"data": list})
    else:
        return HttpResponseRedirect('openuserdashboard')

def vieworders(request):
    request.session['page'] = 'vieworders'
    return render(request,'vieworders.html')
def fetchorders(request):
    mobile=request.GET['mobile']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from myorder where mobile='"+str(mobile)+"'"
    cr.execute(query)
    result = cr.fetchall()
    list = []
    for row in result:
        list.append(row)
    return JsonResponse(list, safe=False)

def orderdetail(request):
    orderid = request.GET['orderid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from orderdetail where orderid='" + str(orderid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    serialno=1
    totalprice=0
    for row in result:
        d={}
        d['serialno']=serialno
        d['detailid']=row[0]
        d['orderid'] = row[1]
        d['pid'] = row[2]
        d['name'] = row[3]
        d['quantity'] = row[4]
        d['sp'] = row[5]
        d['discount'] = row[6]
        d['netprice'] = row[7]
        d['totalprice'] = row[8]
        totalprice=totalprice+row[8]
        x.append(d)
        serialno=serialno+1
    list=[]
    list.append(x)
    list.append(totalprice)
    request.session['page'] = 'orderdetail'

    return render(request,'orderdetail.html',{"data":list})

def getallproducts(request):
    conn = myconnection.connect('')
    s = "select DISTINCT pname from products"
    cr = conn.cursor()
    cr.execute(s)
    res = cr.fetchall()
    conn.commit()
    print(res)
    x = []
    for row in res:
        x.append(row[0])
    return JsonResponse(x, safe=False)
def gotoproductdetailfromhome(request):
    pname = request.GET['Search']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query1="select pid from products where pname='"+str(pname)+"'"
    cr.execute(query1)
    rs=cr.fetchone()
    pid=rs[0]
    query = "select * from photos where pid='" + str(pid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    for row in result:
        d = {}
        d['photoid'] = row[0]
        d['pid'] = row[1]
        d['photopath'] = row[2]
        d['type'] = row[3]
        x.append(d)
    list = []
    list.append(x)
    query = "select * from products where pid='" + str(pid) + "'"
    cr.execute(query)
    row = cr.fetchone()
    d = {}
    d['pid'] = pid
    d['pname'] = row[1]
    d['description'] = row[2]
    d['cp'] = row[3]
    d['sp'] = row[4]
    d['discount'] = row[5]
    d['photo'] = row[6]
    d['quantity'] = row[7]
    d['cname'] = row[8]
    list.append(d)
    return render(request, 'productdetail.html', {"data": list})
