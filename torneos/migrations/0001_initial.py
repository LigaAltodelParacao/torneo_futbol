from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cancha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipos', to='torneos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('en_vivo', models.BooleanField(default=False)),
                ('terminado', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('period', models.IntegerField(default=0)),
                ('minuto_actual', models.IntegerField(default=0)),
                ('cancha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneos.cancha')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('amarillas', models.IntegerField(default=0)),
                ('rojas', models.IntegerField(default=0)),
                ('goles', models.IntegerField(default=0)),
                ('suspendido', models.BooleanField(default=False)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugadores', to='torneos.equipo')),
            ],
        ),
        migrations.AddField(
            model_name='partido',
            name='equipo_local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_local', to='torneos.equipo'),
        ),
        migrations.AddField(
            model_name='partido',
            name='equipo_visitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_visitante', to='torneos.equipo'),
        ),
        migrations.CreateModel(
            name='EventoPartido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minuto', models.IntegerField()),
                ('tipo', models.CharField(choices=[('gol', 'Gol'), ('amarilla', 'Amarilla'), ('roja', 'Roja')], max_length=20)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='torneos.jugador')),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='torneos.partido')),
            ],
        ),
    ]
