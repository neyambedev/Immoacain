from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immo2app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='nom_location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='terrain',
            name='categorie_location',
            field=models.CharField(
                blank=True,
                choices=[
                    ('hotel', 'Hôtel'),
                    ('appartement', 'Appartement'),
                    ('chambre', 'Chambre'),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='terrain',
            name='superficie',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
