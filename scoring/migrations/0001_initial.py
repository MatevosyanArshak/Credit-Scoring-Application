from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(max_length=10)),
                ('family_members', models.IntegerField()),
                ('monthly_income', models.IntegerField()),
                ('credit_history', models.IntegerField()),
                ('loan_type', models.IntegerField()),
                ('loan_term', models.IntegerField()),
                ('loan_amount', models.IntegerField()),
                ('mortgage_type', models.IntegerField()),
                ('prob_default', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
