from django.db import models
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=3)
    currency = models.CharField(max_length=30)
    currency_code = models.CharField(max_length=3)
    currency_symbol = models.CharField(max_length=3)

    @classmethod
    def get_country_from_code(cls, code):
        country = cls.objects.filter(code=code)
        if country.exists():
            return country.latest('id')

        return cls.objects.get(code="GB")

    def __str__(self):
        return f'{self.name} ({self.code})'


class Product(models.Model):
    name = models.CharField(max_length=30)


class Supplier(models.Model):
    name = models.CharField(max_length=30)


class Customer(models.Model):
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)


class Dealership(models.Model):
    name = models.CharField(max_length=30)


class AssociatedProducts(models.Model):
    dealership = models.ForeignKey(Dealership, related_name='associated_products_dealership',
                                   blank=False, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, related_name='associated_products_product',
                                blank=False, on_delete=models.DO_NOTHING)


class Application(models.Model):
    dealership = models.ForeignKey(Dealership, related_name='dealerships', blank=False, default='1',
                                   on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, related_name='app_country', null=False, blank=False,
                                on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, related_name='customer', blank=True, null=True, on_delete=models.DO_NOTHING)


class SupplierApplication(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='sa_supplier', blank=False, null=False,
                                 on_delete=models.DO_NOTHING)
    dealership = models.ForeignKey(Dealership, related_name='sa_dealership', blank=False, null=False,
                                   on_delete=models.DO_NOTHING)
    expired = models.BooleanField(default=False)
    token = models.CharField(max_length=36)
    signature = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)
    supplier_success_url = models.CharField(max_length=1000)
    supplier_failure_url = models.CharField(max_length=1000)
    forename = models.CharField(max_length=254, blank=True, null=True)
    surname = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    vehiclereg = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=14, blank=True, null=True)
    subbuildingname = models.CharField(max_length=200, blank=True, null=True)
    buildingname = models.CharField(max_length=200, blank=True, null=True)
    buildingnumber = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    town = models.CharField(max_length=200, blank=True, null=True)
    county = models.CharField(max_length=200, blank=True, null=True)
    country = models.ForeignKey(Country, related_name='supplier_country', null=True, blank=True,
                                on_delete=models.DO_NOTHING)
    postcode = models.CharField(max_length=200, blank=True, null=True)
    application_product = models.ForeignKey(Product, related_name='sa_product', blank=True, null=True,
                                            on_delete=models.DO_NOTHING)
    application = models.ForeignKey(Application, related_name='sa_application', blank=True, null=True,
                                    on_delete=models.DO_NOTHING)


class AssociatedSupplierDealerships(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='associated_sd_supplier', blank=False, on_delete=models.DO_NOTHING)
    dealership = models.ForeignKey(Dealership, related_name='associated_sd_dealership', blank=False, on_delete=models.DO_NOTHING)
    apikey = models.CharField(max_length=30, unique=True)
    live_date = models.DateField(default=timezone.now)
