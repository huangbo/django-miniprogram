from django.db import models


class PaymentModel(models.Model):
    """ PaymentModel
    An abstract base class model that provides payment common fields.
    """
    price = models.FloatField(default=0)
    discount = models.FloatField(default=1)

    @property
    def discount_price(self):
        return str(int(self.price * self.discount * 100))

    @property
    def payment_body(self):
        return self.name if hasattr(self, "name") else ""

    @property
    def payment_detail(self):
        return ""

    @property
    def payment_attach(self):
        return ""

    class Meta:
        abstract = True
