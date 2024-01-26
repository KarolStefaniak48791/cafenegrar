# Generated by Django 5.0 on 2024-01-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewhub', '0016_delete_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_ids', models.CharField(max_length=255)),
                ('number_of_hours', models.IntegerField()),
                ('selected_date', models.DateField()),
                ('reservation_cost', models.FloatField()),
            ],
        ),
    ]
