from django.db import migrations


def create_subjects(apps, schema_editor):
    Subject = apps.get_model('account', 'Subject')
    Subject.objects.create(name='Python', color='#343a40')
    Subject.objects.create(name='Django', color='#007bff')
    Subject.objects.create(name='Algoritms', color='#28a745')

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_subjects),
    ]
