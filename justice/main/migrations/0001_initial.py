from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('subject', models.CharField(max_length=200)),
                ('service', models.CharField(blank=True, choices=[('', 'Select a Service'), ('family', 'Family Law'), ('criminal', 'Criminal Law'), ('civil', 'Civil Law'), ('corporate', 'Corporate Law'), ('real-estate', 'Real Estate Law'), ('employment', 'Employment Law'), ('other', 'Other')], max_length=30)),
                ('message', models.TextField()),
                ('terms', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
