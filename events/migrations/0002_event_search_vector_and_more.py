# Generated by Django 5.0.1 on 2024-02-04 18:55

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.AddIndex(
            model_name='event',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='events_even_search__5f308c_gin'),
        ),
    ]