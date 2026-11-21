# import black
# from django.core.validators import MinValueValidator
# from django.db import models
#
# from models import OrganizationScopedModel
#
#
# class Direction(models.TextChoices):
#     RECEIVED = "received"
#     ISSUED = "issued"
#
#
# class Medium(models.TextChoices):
#     PHYSICAL = "physical"
#     ELECTRONICAL = "electronical"
#
#
# class Purpose(models.TextChoices):
#     PAYMENT = "payment"
#     SECURITY = "security"
#     SAFEKEEPING = "safekeeping"
#
#
# class ReceivedStatus(models.TextChoices):
#     RECEIVED = "received"
#     DEPOSITED = "deposited"
#     CLEARED = "cleard"
#     BOUNCED = "bounced"
#     RETURNED = "returned"
#
#
# class IssuedStatus(models.TextChoices):
#     ISSUED = "issued"
#     CLEARD = "cleared"
#     BOUNCED = "bounced"
#     CANCELED = "canceled"
#
#
# STATUS_CHOICES = dict(ReceivedStatus.choices + IssuedStatus.choices)
#
#
# class Check(OrganizationScopedModel):
#     direction = models.CharField(max_length=8, choices=Direction.choices)
#     identifier = models.CharField(max_length=64)
#     amount = models.DecimalField(
#         max_digits=18,
#         decimal_places=0,
#         validators=[MinValueValidator(1)],
#     )
#     due_date = models.DateField()
#     medium = models.CharField(max_length=12, choices=Medium.choices)
#     purpose = models.CharField(max_length=12, choices=Purpose.choices)
#     status = models.CharField(max_length=12, choices=STATUS_CHOICES)
#     holder = models.ForeignKey(
#         "organization.OrganizationMembership",
#         on_delete=models.PROTECT,
#         null=True,
#         blank=True,
#     )
