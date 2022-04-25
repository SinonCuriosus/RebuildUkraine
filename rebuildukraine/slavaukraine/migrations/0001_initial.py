# Generated by Django 4.0.4 on 2022-04-25 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('profile_image', models.FileField(blank=True, null=True, upload_to='')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_person', models.BooleanField(default=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Binary', 'Binary'), ('Nonbinary', 'Nonbinary'), ('Other', 'Other')], max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Utilizadores singulares',
                'verbose_name_plural': 'Utilizadores singulares',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('Kiev', 'Kiev'), ('Kharkiv', 'Kharkiv'), ('Mariupol', 'Mariupol')], max_length=25)),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('Ucrânia', 'Ucrânia')], max_length=25)),
            ],
            options={
                'verbose_name': 'País',
                'verbose_name_plural': 'Países',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('taxnumber', models.CharField(max_length=9, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_enterpise', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertiseSubject', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Especialização',
                'verbose_name_plural': 'Especializações',
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slavaukraine.city')),
                ('enterprise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='slavaukraine.enterprise')),
                ('expertiseNeeded', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='slavaukraine.expertise')),
            ],
            options={
                'verbose_name': 'Proposta de voluntariado',
                'verbose_name_plural': 'Propostas de voluntariado',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.ManyToManyField(to='slavaukraine.expertise')),
                ('person', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Voluntário especialista',
                'verbose_name_plural': 'Voluntários especializados',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ManyToManyField(to='slavaukraine.proposal')),
            ],
            options={
                'verbose_name': 'Registo em voluntariado',
                'verbose_name_plural': 'Registos em voluntariados',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ManyToManyField(to='slavaukraine.proposal')),
            ],
            options={
                'verbose_name': 'Favorito',
                'verbose_name_plural': 'Favoritos',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slavaukraine.country'),
        ),
    ]
