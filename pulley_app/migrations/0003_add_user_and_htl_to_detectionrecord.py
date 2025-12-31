# Generated manually to add user and htl_value fields to DetectionRecord

from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pulley_app", "0002_remove_detectionrecord_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="detectionrecord",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="User who initiated the live detection",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="detection_records",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="detectionrecord",
            name="htl_value",
            field=models.FloatField(
                blank=True,
                help_text="HTL (L/2) value used for calculation",
                null=True,
            ),
        ),
    ]

