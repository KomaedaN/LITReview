# Generated by Django 3.2.16 on 2022-10-30 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='review.ticket'),
            preserve_default=False,
        ),
    ]