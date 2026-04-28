from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_memberprofile_show_in_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='Telefon'),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='interest',
            field=models.CharField(
                blank=True,
                choices=[
                    ('', '—'),
                    ('catalog', 'Catalog / Modele'),
                    ('comunitate', 'Comunitate / Forum'),
                    ('evenimente', 'Evenimente / Tururi'),
                    ('altele', 'Altele'),
                ],
                max_length=50,
                verbose_name='Interes',
            ),
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='email',
            field=models.EmailField(blank=True, verbose_name='Email'),
        ),
    ]
