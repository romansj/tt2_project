# Generated by Django 3.0.6 on 2020-06-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='ingredients',
            field=models.ManyToManyField(blank=True, null=True, to='recipes.Ingredient'),
        ),
    ]