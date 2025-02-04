# Generated by Django 5.0.7 on 2024-07-15 23:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nombre', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('saldo', models.CharField(max_length=100)),
                ('NumerosContacto', models.TextField(default='[]')),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino', to='mensajeria.usuario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensajeria.usuario')),
            ],
        ),
    ]
