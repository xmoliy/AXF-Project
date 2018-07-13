from django.db import models


# Create your models here.
class TopModel(models.Model):
    trackid = models.CharField(primary_key=True, max_length=10)
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class TopWheel(TopModel):
    class Meta:
        db_table = 'axf_wheel'  # 指定表名


class TopMenu(TopModel):
    positon = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_nav'


class Mustbuy(TopModel):
    class Meta:
        db_table = 'axf_mustbuy'


class Shop(TopModel):
    positon = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_shop'


class MainShowBrand(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    class Meta:
        db_table = 'axf_brand'


class BrandProduct(models.Model):
    img = models.CharField(max_length=100)
    childcid = models.CharField(max_length=10)
    productid = models.CharField(max_length=10)
    longname = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    marketprice = models.CharField(max_length=10)
    brand = models.ForeignKey(MainShowBrand, on_delete=models.CASCADE)

    class Meta:
        db_table = 'axf_brand_product'


# 食品分类
class FoodType(models.Model):
    typeid = models.CharField(primary_key=True, max_length=50)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(primary_key=True, max_length=10)
    productimg = models.CharField(max_length=300)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=100)
    isxf = models.BooleanField(default=1)
    pmdesc = models.IntegerField(default=1)
    specifics = models.CharField(max_length=100)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    marketprice = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=10)
    storenums = models.IntegerField(default=1)
    productnum = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'


class UserManager(models.ManyToManyField):
    def get_queryset(self):
        return super().get_queryset().filter(stat=True)


class User(models.Model):
    userName = models.CharField(max_length=50)
    userPasswd = models.CharField(max_length=32)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=50, default='')
    nickName = models.CharField(max_length=50, verbose_name='昵称')
    imgpath = models.CharField(max_length=100, default='')
    token = models.CharField(max_length=32, default='')
    state = models.BooleanField(default=True, verbose_name='用户状态')
    money = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    object = UserManager

    def delete(self, using=None, keep_parents=False):
        self.state = False
        self.save()
        return '已注销'

    class Meta:
        db_table = 'axf_user'


class DeliveryAddress(models.Model):
    #  收件地址模型
    name = models.CharField(max_length=20, verbose_name='收件人')
    phone = models.CharField(max_length=20, verbose_name='收件人电话')
    address_detail = models.TextField(default='', verbose_name='收货地址')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'axf_address'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    #  数量
    cnt = models.IntegerField(default=1)

    # 是否被选中
    isSelected = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #  订单的收货地址
    orderAddress = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    #  订单的单号
    orderNum = models.CharField(primary_key=True, max_length=50, verbose_name='订单号')
    # 订单的总金额
    orderPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # 订单的支付状态
    pay_states = ((0, '待支付'), (1, '已支付'), (2, '正在支付中'), ((3, '已退款')))
    payState = models.IntegerField(choices=pay_states, default=0)

    #支付的方式
    pay_types=((0,'余额'),(1,'支付宝'),(2,'微信'))
    payType = models.IntegerField(choices=pay_types,default=0)



    @property
    def payStateName(self):
        return self.pay_states[self.payState][1]

    # 订单派送状态
    order_states = ((0, '待派送'), (1, '已派送'), (2, '已送达'), (3, '已签收'), (4, '拒收'))
    orderState = models.IntegerField(choices=order_states, default=0)

    @property
    def orderStateName(self):
        return self.order_states[self.orderState][1]

    orderTime = models.DateTimeField(auto_now_add=True)
    orderLastTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'


class OrderGoods(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.SET_NULL,null=True)
    cnt = models.IntegerField(default=1)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='小计')
    class Meta:
        db_table='axf_order_goods'
