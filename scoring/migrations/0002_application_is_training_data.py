from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_training_data',
            field=models.BooleanField(default=False),
        ),
    ]
