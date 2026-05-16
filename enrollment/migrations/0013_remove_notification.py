from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0012_notification_message_notification_notif_type_and_more'),
        ('notificaciones', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Notification',
                ),
            ],
        ),
    ]
