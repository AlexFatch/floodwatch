from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('monitor', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='rain_rate_mm_h',
            field=models.FloatField(blank=True, null=True),
        ),
    ]