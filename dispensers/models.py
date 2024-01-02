import uuid
from django.db import models
from django.db.models.signals import pre_save, m2m_changed,post_save

from users.models import User
from products.models import Product

class Dispenser(models.Model):
    dispenser_id=models.CharField(max_length=100, null=False, blank=False, unique=True)
    user=models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='DispenserProducts')
    total=models.DecimalField(default=0, max_digits=8, decimal_places=0)
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Dispensador")
        verbose_name_plural = ("Dispensadores")
    def __str__(self):
        return self.dispenser_id
    
    def update_totals(self):
        self.update_total()

    def update_total(self):
        self.total = sum([(cp.product.precio / cp.product.cantidad_caja * cp.quantity) for cp in self.products_related()])
        self.save()

    def products_related(self):
        return self.dispenserproducts_set.select_related('product').all()
    
    def register_withdrawal(self, user):
        for cp in self.products_related():
            product = cp.product
            product.existencia -= cp.quantity
            product.save()
        

class DispenserProductsManger(models.Manager):
    def create_or_update_quantity(self, dispenser, product, quantity=1):
        object, created = self.get_or_create(dispenser=dispenser, product=product)
        if not created:
            quantity = object.quantity + int(quantity) 
        object.update_quantity(quantity)
        return object
      
class DispenserProducts(models.Model):
    dispenser=models.ForeignKey(Dispenser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects=DispenserProductsManger()

    def update_quantity(self,quantity=1):
        self.quantity=quantity
        self.save()

def set_dispenser_id(sender, instance, *args, **kwargs):
    if not instance.dispenser_id:
        instance.dispenser_id=str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action=='post_add' or action=='post_remove' or action =='post_clear':
        instance.update_totals()

def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.dispenser.update_totals()

pre_save.connect(set_dispenser_id, sender=Dispenser)
post_save.connect(post_save_update_totals, sender=DispenserProducts)
m2m_changed.connect(update_totals,sender=Dispenser.products.through)

