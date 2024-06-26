# Generated by Django 5.0.3 on 2024-05-13 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0003_remove_stockdata_adj_close'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdata',
            name='Close',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='High',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='Low',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='Open',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='Volume',
            field=models.IntegerField(),
        ),
    ]
