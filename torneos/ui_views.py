from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone
from .models import Partido, Jugador, EventoPartido

def live_view(request):
    return render(request, 'live_view.html')

def viewer_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    return render(request, 'viewer_partido.html', {'partido': partido})

@staff_member_required
def admin_partido_control(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    return render(request, 'admin_partido_control.html', {'partido': partido})

@staff_member_required
@csrf_exempt
def api_toggle_start(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    data = json.loads(request.body.decode('utf-8') or '{}')
    action = data.get('action')
    if action == 'start':
        partido.en_vivo = True
        partido.start_time = timezone.now()
        partido.period = 1
        partido.save()
        return JsonResponse({'status':'started','period':1})
    if action == 'end_period':
        if partido.period == 1:
            partido.period = 2; partido.en_vivo = False; partido.save()
            return JsonResponse({'status':'half_time'})
        elif partido.period == 3:
            partido.period = 4; partido.en_vivo = False; partido.terminado = True; partido.save()
            return JsonResponse({'status':'ended'})
    if action == 'start_second':
        partido.period = 3; partido.start_time = timezone.now(); partido.en_vivo = True; partido.save()
        return JsonResponse({'status':'second_started'})
    return JsonResponse({'error':'unknown action'}, status=400)

@staff_member_required
@csrf_exempt
def api_send_event(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    payload = json.loads(request.body.decode('utf-8') or '{}')
    tipo = payload.get('tipo'); minuto = payload.get('minuto'); jugador_id = payload.get('jugador_id')
    if not tipo or minuto is None or not jugador_id:
        return JsonResponse({'error':'faltan datos'}, status=400)
    jugador = get_object_or_404(Jugador, id=jugador_id)
    ev = EventoPartido.objects.create(partido=partido, minuto=minuto, jugador=jugador, tipo=tipo)
    if tipo == 'gol': jugador.goles += 1
    elif tipo == 'amarilla': jugador.amarillas += 1
    elif tipo == 'roja': jugador.rojas += 1
    jugador.save()
    return JsonResponse({'ok': True, 'evento_id': ev.id})
