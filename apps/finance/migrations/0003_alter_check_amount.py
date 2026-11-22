import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0002_checkstatus_checktype_check"),
    ]

    operations = [
        migrations.AlterField(
            model_name="check",
            name="amount",
            field=models.DecimalField(
                validators=[django.core.validators.DecimalValidator(None, 2)]
            ),
        ),
    ]
