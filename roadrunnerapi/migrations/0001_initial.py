# Generated by Django 4.0.3 on 2022-03-10 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('user_type', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Endorsement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='FreightType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('pickup_city', models.CharField(max_length=300)),
                ('pickup_state', models.CharField(max_length=30)),
                ('pickup_datetime', models.DateTimeField()),
                ('dropoff_city', models.CharField(max_length=300)),
                ('dropoff_state', models.CharField(max_length=30)),
                ('dropoff_datetime', models.DateTimeField()),
                ('distance', models.PositiveIntegerField()),
                ('is_hazardous', models.BooleanField()),
                ('is_booked', models.BooleanField()),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='LoadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='TrailerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=120)),
                ('current_city', models.CharField(max_length=300)),
                ('current_state', models.CharField(max_length=30)),
                ('is_assigned', models.BooleanField(default=False)),
                ('dispatcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='TruckEndorsement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endorsement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.endorsement')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.truck')),
            ],
        ),
        migrations.AddField(
            model_name='truck',
            name='endorsements',
            field=models.ManyToManyField(related_name='endorsements', through='roadrunnerapi.TruckEndorsement', to='roadrunnerapi.endorsement'),
        ),
        migrations.AddField(
            model_name='truck',
            name='trailer_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.trailertype'),
        ),
        migrations.CreateModel(
            name='LoadFreightType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freight_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.freighttype')),
                ('load', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.load')),
            ],
        ),
        migrations.AddField(
            model_name='load',
            name='freight_types',
            field=models.ManyToManyField(related_name='freight_types', through='roadrunnerapi.LoadFreightType', to='roadrunnerapi.freighttype'),
        ),
        migrations.AddField(
            model_name='load',
            name='load_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.loadstatus'),
        ),
        migrations.CreateModel(
            name='DispatcherRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating', models.PositiveSmallIntegerField()),
                ('dispatcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispatcher', to='roadrunnerapi.appuser')),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distributor', to='roadrunnerapi.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollar_amount', models.FloatField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('dispatcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.appuser')),
                ('load', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.load')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadrunnerapi.truck')),
            ],
        ),
    ]
