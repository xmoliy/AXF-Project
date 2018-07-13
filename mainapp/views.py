import hashlib
import os
import time
from uuid import uuid4

from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from AXF_project import settings
from mainapp.models import TopWheel, TopMenu, Mustbuy, Shop, MainShowBrand, FoodType, Goods, User, DeliveryAddress, \
    Cart, Order, OrderGoods


def home(req):
    shopList = Shop.objects.all().order_by('positon')
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    return render(req, 'home.html', {'title': '主页',
                                     'topWheels': TopWheel.objects.all(),
                                     'topmenus': TopMenu.objects.all().order_by('positon'),
                                     'mustbuyList': Mustbuy.objects.all(),
                                     'shop1': shop1,
                                     'shop2': shop2,
                                     'shop3': shop3,
                                     'shop4': shop4,
                                     'mainList': MainShowBrand.objects.all()})


def market(req, categoryid=0, childcid=0, sortid=0):
    goodsList = None
    # 获取所有子类型
    childTypes = []
    if categoryid:
        cTypes = FoodType.objects.filter(typeid=categoryid).last().childtypenames
        cTypes = cTypes.split('#')
        for ctype in cTypes:
            ctype = ctype.split(':')
            childTypes.append({'name': ctype[0], 'id': ctype[1]})
        if childcid:
            goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childcid).order_by('productid')
        else:
            goodsList = Goods.objects.filter(categoryid=categoryid).order_by('productid')
    else:
        goodsList = Goods.objects.all()[0:20]

    if sortid == 1:
        goodsList = goodsList.order_by('-price')
    elif sortid == 2:
        goodsList = goodsList.order_by('price')
    elif sortid == 3:
        goodsList = goodsList.order_by('-productnum')

    return render(req, 'market.html',
                  {'title': '闪购',
                   'foodtypes': FoodType.objects.all(),
                   'goodsList': goodsList,
                   'categoryid': str(categoryid),
                   'childTypes': childTypes,
                   'childcid': str(childcid),
                   'sortid': sortid})


def cart(req):
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req, 'login.html', {'title': '用户登录'})
    deliveryAddress = DeliveryAddress.objects.filter(user_id=user_id).first()
    carts = Cart.objects.filter(user_id=user_id)
    totalPrice = 0
    for cart in carts:
        if cart.isSelected:
            totalPrice += cart.goods.price * cart.cnt
    return render(req, 'cart.html',
                  {'title': '购物车',
                   'myAddress': deliveryAddress,
                   'carts': carts,
                   'totalPrice': totalPrice})


def mine(req):
    # if req.COOKIES.get('token'):
    #     return redirect('/app/login')
    print(req.COOKIES.get('token'))
    return render(req, 'mine.html',
                  {'title': '我的',
                   'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu(),
                   'loginUser': User.objects.filter(token=req.COOKIES.get('token')).last})


def getMyOrderNav():
    navs = []
    navs.append({'name': '待付款', 'icon': 'glyphicon glyphicon-usd', 'url': '/app/noPayOrder/0'})
    navs.append({'name': '待收货', 'icon': 'glyphicon glyphicon-envelope', 'url': '/app/noPayOrder/1'})
    navs.append({'name': '待评价', 'icon': 'glyphicon glyphicon-pencil', 'url': ''})
    navs.append({'name': '退款/售后', 'icon': 'glyphicon glyphicon-retweet', 'url': ''})
    return navs


def getMyOrderMenu():
    menus = []
    menus.append({'name': '积分商城', 'icon': 'glyphicon glyphicon-bullhorn', 'url': ''})
    menus.append({'name': '优惠券', 'icon': 'glyphicon glyphicon-credit-card', 'url': ''})
    menus.append({'name': '收货地址', 'icon': 'glyphicon glyphicon-import', 'url': '/app/address'})
    menus.append({'name': '客服/反馈', 'icon': 'glyphicon glyphicon-phone-alt', 'url': ''})
    menus.append({'name': '关于我们', 'icon': 'glyphicon glyphicon-asterisk', 'url': ''})
    return menus


def register(req):
    if req.method == 'GET':
        return render(req, 'regist.html')
    user = User()
    user.userName = req.POST.get('username')
    user.userPasswd = crypt(req.POST.get('passwd'))
    user.nickName = req.POST.get('nickname')
    user.phone = req.POST.get('phone')
    user.token = newToken(user.userName)
    user.save()

    resp = redirect('/app/mine')
    resp.set_cookie('token', user.token)
    return resp


@csrf_exempt  # 不做CSRF_token验证
def upload(req):
    msg = {}
    cookie_token = req.COOKIES.get('token')
    if not cookie_token:
        msg['state'] = 'fail'
        msg['msg'] = '请先登录'
        msg['code'] = '201'

    else:
        qs = User.objects.filter(token=cookie_token)
        if not qs.exists():
            msg['state'] = 'fail'
            msg['msg'] = '登录失效，请重新登录'
            msg['code'] = '202'
        else:
            # 开始上传
            uploadFile = req.FILES.get('img')
            saveFileName = newFileName(uploadFile.content_type)
            saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)
            with open(saveFilePath, 'wb') as  f:
                for part in uploadFile.chunks():
                    f.write(part)
                    f.flush()
            # 将上传文件的路径更新到用户
            qs.update(imgpath='uploads/' + saveFileName)
            msg['state'] = 'ok'
            msg['msg'] = '上传成功'
            msg['code'] = '200'
            msg['path'] = 'uploads/' + saveFileName

    return JsonResponse(msg)


def newFileName(contentType):
    fileName = crypt(str(uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName = '.png'
    return fileName + extName


def newToken(userName):
    md5 = hashlib.md5()
    md5.update((str(uuid4()) + userName).encode())
    return md5.hexdigest()


def crypt(pwd, cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    username = req.POST.get('username')
    passwd = crypt(req.POST.get('passwd'))

    user = User.objects.filter(userName=username, userPasswd=passwd)
    if not user.exists():
        return render(req, 'login.html', {'msg': '用户或密码错误'})
    user = user.last()
    print(user.userName)
    req.session['user_id'] = user.id
    user.token = newToken(user.userName)
    user.save()
    resp = redirect('/app/mine')
    resp.set_cookie('token', user.token)
    return resp


def logout(req):
    token = req.COOKIES.get('token')
    if token:
        try:
            user = User.objects.get(token=token)
            user.token = ''
            user.save()
            resp = redirect('/app/mine')
            resp.delete_cookie('token')
            return resp
        except:
            pass
    return render(req, 'logout.html', {'msg': '退出失败，您可能还没登录'})


def selectCart(req, cart_id):
    if cart_id == 0 or cart_id == 99999:  # 0全选 -1取消全选
        #  全部更新
        carts = Cart.objects.filter(user_id=req.session.get('user_id'))
        carts.update(isSelected=True if cart_id == 0 else False)
        totalPrice = 0
        if cart_id == 0:
            for cart in carts:
                totalPrice += cart.cnt * cart.goods.price

        return JsonResponse({'price': totalPrice, 'status': 200})
    data = {'status': 200, 'price': 1000}
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.isSelected = not cart.isSelected
        cart.save()
        data['price'] = cart.cnt * cart.goods.price
        data['selected'] = cart.isSelected  # 当前选择状态
    except:
        data['status'] = 300
        data['price'] = 0
    return JsonResponse(data)


def addCart(req, cart_id):
    # 添加指定card_id的商品信息    如果cart_id不存在是 要新添加
    price = 0
    if Cart.objects.filter(id=cart_id).exists():
        Cart.objects.filter(id=cart_id).update(cnt=F('cnt') + 1)
        price = Cart.objects.filter(id=cart_id).last().goods.price
        return JsonResponse({'status': 200, 'price': price})
    else:
        # 如果cart_id不存在时 要新添加商品
        user_id = req.session.get('user_id')
        if Cart.objects.filter(goods_id=cart_id, user_id=user_id).exists():
            Cart.objects.filter(goods_id=cart_id, user_id=user_id).update(cnt=F('cnt') + 1)
            price = Cart.objects.filter(goods_id=cart_id, user_id=user_id).last().goods.price
        else:

            #  要新添加商品
            cart = Cart()
            cart.cnt = 1
            cart.user_id = user_id
            cart.goods_id = cart_id
            cart.save()
            price = Cart.objects.filter(goods_id=cart_id).last().goods.price
    return JsonResponse({'status': 200, 'price': price})


def subCart(req, cart_id):
    # 减掉指定card_id的商品信息
    price = 0
    cartCnt = Cart.objects.filter(id=cart_id).last().cnt
    if cartCnt > 1:
        Cart.objects.filter(id=cart_id).update(cnt=F('cnt') - 1)
        price = Cart.objects.filter(id=cart_id).last().goods.price
        return JsonResponse({'status': 200, 'price': price})


def order(req, num):
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req, 'login.html')
    order = None
    if num == '0':
        order = Order()
        order.user_id = user_id
        #  获取用户的第一个收货地址，作为订单的收货地址
        order.orderAddress_id = User.objects.get(pk=user_id).deliveryaddress_set.first().pk

        #  设置订单号
        order.orderNum = createOrderNum()

        # 设置订单金额
        # 1.查询当前用户下的所有购物车的商品
        carts = Cart.objects.filter(isSelected=True, user_id=user_id)

        if carts.count() == 0:
            return redirect('/app/cart')
        order.save()
        # 2.统计订单总金额 和将商品插入到order页面中
        order.orderPrice = 0
        for cart in carts:
            order.orderPrice += cart.cnt * cart.goods.price

            # 创建订单明细对象
            ordergoods = OrderGoods()
            ordergoods.order_id = order.orderNum
            ordergoods.goods_id = cart.goods.pk
            ordergoods.cnt = cart.cnt
            ordergoods.price = cart.cnt * cart.goods.price
            ordergoods.save()

        order.save()
        carts.delete()  # 删除购物车中的商品
    else:  # 查询订单
        order = Order.objects.filter(pk=num)
    return render(req, 'order.html', {'title': '我的订单', 'order': order})


def createOrderNum():
    orderNum = '0029' + str(time.time()).replace('.', '')[-8:]
    return orderNum


def pay(req, num, payType=0):
    try:
        order = Order.objects.get(pk=num)
        order.pay_type = payType

        user = User.objects.get(pk=req.session.get('user_id'))

        if user.money < order.orderPrice:
            return JsonResponse({'status': 'fail', 'msg': '钱不够'})
        else:
            user.money -= order.orderPrice
            user.save()
            order.payType = 1
            order.save()

            # 减去库存
            # 优化业务，在添加到购物车时候，判断商品的库存量
            for item in order.ordergoods_set.all():
                goods = item.goods
                goods.productnum += item.cnt  # 销售量 加
                goods.storenums -= item.cnt  # 库存量 减
                goods.save()
    except:
        return JsonResponse({'status': 'fail', 'msg': '支付失败'})

    return JsonResponse({'status': 'ok', 'msg': '支付成功'})


def noPayOrder(req,condition):
    user_id = req.session.get('user_id')
    if condition==0:
        datas = Order.objects.filter(payState=0,user_id=user_id)
        return render(req, 'noPayOrder.html', {'datas': datas})
    elif condition==1:
        datas = Order.objects.filter(orderState__in=(0,1), user_id=user_id)
        return render(req,'receiving.html',{'datas':datas})

def address(req):
    user_id= req.session.get('user_id')
    datas = DeliveryAddress.objects.filter(user_id=user_id)
    return render(req,'address.html',{'datas':datas})


def editAddress(req):
    user_id= req.session.get('user_id')
    if not user_id:
        return render(req, 'login.html')
    if req.method =='GET':
        id=req.GET.get('id')
        return render(req,'editAddress.html',{'data':DeliveryAddress.objects.filter(user_id=user_id,id=id).first()})
    id = req.POST.get('id')
    print(id)
    name =req.POST.get('username')
    phone= req.POST.get('phone')
    address_detail = req.POST.get('address_detail')
    if id:
        DeliveryAddress.objects.filter(user_id=user_id, id=id).update(name=name,phone=phone,address_detail=address_detail)
    else:
        DeliveryAddress.objects.create(name=name,phone=phone,address_detail=address_detail,user_id=user_id)
    return HttpResponse('<h4>操作成功!</h4><a href="/app/address">查看列表</a>')

def addAddress(req):
    return render(req,'editAddress.html')


def delAddress(req):
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req, 'login.html')
    id = req.GET.get('id')
    if id:
        DeliveryAddress.objects.filter(id=id,user_id=user_id).delete()
    return HttpResponse('<h4>删除成功!</h4><a href="/app/address">查看列表</a>')