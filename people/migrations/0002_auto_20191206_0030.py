# Generated by Django 2.2.7 on 2019-12-06 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("people", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="friends",
            field=models.ManyToManyField(
                related_name="_person_friends_+", to="people.Person"
            ),
        )
    ]