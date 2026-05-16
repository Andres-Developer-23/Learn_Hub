from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enrollment', '0012_notification_message_notification_notif_type_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Notification',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('title', models.CharField(default='Notificación', max_length=200)),
                        ('message', models.TextField(blank=True, default='')),
                        ('notif_type', models.CharField(choices=[('info', 'Información'), ('success', 'Éxito'), ('warning', 'Advertencia'), ('error', 'Error')], default='info', max_length=20)),
                        ('is_read', models.BooleanField(default=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='enrollment.student')),
                    ],
                    options={
                        'ordering': ['-created_at'],
                        'db_table': 'enrollment_notification',
                    },
                ),
            ],
        ),
    ]
