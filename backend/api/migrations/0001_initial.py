from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('status_code', models.IntegerField(blank=True, null=True)),
                ('response_time', models.FloatField(blank=True, null=True)),
                ('is_reachable', models.BooleanField(default=False)),
                ('error_message', models.TextField(blank=True)),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('batch_id', models.UUIDField(default=uuid.uuid4)),
            ],
            options={
                'ordering': ['-checked_at'],
                'indexes': [
                    models.Index(fields=['batch_id'], name='api_urlchec_batch_i_0e6ed4_idx'),
                    models.Index(fields=['checked_at'], name='api_urlchec_checked_5e6ed4_idx'),
                ],
            },
        ),
    ]