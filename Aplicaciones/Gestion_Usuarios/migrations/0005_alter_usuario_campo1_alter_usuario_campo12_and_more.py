# Generated by Django 5.0.7 on 2024-07-17 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Usuarios', '0004_alter_usuario_campo11'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='campo1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo12',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo13',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo5',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='campo6',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
