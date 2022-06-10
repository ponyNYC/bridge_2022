# Generated by Django 4.0.4 on 2022-06-09 11:37

from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('bridgeapp', 'Category')
    categories = [
        'Pre-commitment',
        'Currently Incarcerated',
        'Post-release',
    ]

    for category in categories:
        Category.objects.create(type=category)

class Migration(migrations.Migration):

    dependencies = [
        ('bridgeapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories)
    ]
