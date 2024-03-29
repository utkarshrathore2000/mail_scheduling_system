# Generated by Django 2.2.7 on 2023-02-11 14:15

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
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('parcel_name', models.CharField(db_index=True, max_length=255)),
                ('parcel_weight', models.DecimalField(decimal_places=2, help_text='weight of the parcel in Kg', max_digits=12)),
                ('parcel_volume', models.DecimalField(decimal_places=2, help_text='volume of the parcel in cm^3', max_digits=12)),
                ('withdraw_bids', models.BooleanField(default=False, help_text='by default it is False when user create a parcel if user withdraw for some reason it will update to True.')),
                ('parcel_owner', models.ForeignKey(help_text='the owner of the parcel who create a parcel for shipping.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'parcel',
            },
        ),
        migrations.CreateModel(
            name='TrainTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('source', models.CharField(help_text='the source name of the track', max_length=255)),
                ('destination', models.CharField(help_text='the destination name of the track', max_length=255)),
                ('is_busy', models.BooleanField(default=False, help_text='by default it is False when post master assigned the lines for any train it will update to True and after three hours it will automatically update to False')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('train_name', models.CharField(help_text='The name of the train', max_length=255)),
                ('capacity', models.DecimalField(decimal_places=2, help_text='capacity of the train', max_digits=12)),
                ('cost', models.DecimalField(decimal_places=2, help_text='the cost of the shipping', max_digits=12)),
                ('is_available', models.BooleanField(default=True, help_text='by default it is True it will update to False when the train will shipped.')),
                ('withdraw_bids', models.BooleanField(default=False, help_text='by default it is False when Train Operator posts an offer for a train if user withdraw for some reason it will update to True.')),
                ('lines_they_operate', models.ManyToManyField(help_text='assigned all lines that train operator can operate', related_name='operate_track', to='shipping_parcel.TrainTrack')),
                ('train_operator', models.ForeignKey(help_text='the operator of the train who can posts an offer for a train', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Train',
            },
        ),
        migrations.CreateModel(
            name='ShippedParcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('assigned_lines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_track', to='shipping_parcel.TrainTrack')),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_parcel', to='shipping_parcel.Parcel')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_train', to='shipping_parcel.Train')),
            ],
            options={
                'db_table': 'ShippedParcel',
            },
        ),
    ]
