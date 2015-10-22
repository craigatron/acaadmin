from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from schedule.models import Event, Attendance

@login_required
def index(request):
    return render(request, 'schedule.html')

@login_required
def event_feed(request):
    events = Event.objects.filter(
        start_time__range=(request.GET.get('start'), request.GET.get('end')))
    results = []
    for e in events:
        event_dict = {'id': e.pk, 'title': e.name, 'start': str(e.start_time)}
        if e.end_time:
            event_dict['end'] = str(e.end_time)
        results.append(event_dict)

    return JsonResponse(results)

@login_required
def event_view(request, event_id):
    event = Event.objects.get(id=event_id)

    d = {'event': event, 'attending': [], 'not_attending': []}

    attendances = Attendance.objects.filter(event=event)
    all_users = list(User.objects.all())
    for a in attendances:
        full_name = ' '.join((a.user.first_name, a.user.last_name))
        d['attending' if a.can_attend else 'not_attending'].append(full_name)
        all_users.remove(a.user)

    d['no_response'] = [' '.join((u.first_name, u.last_name)) for u in all_users]

    return render(request, 'event.html', d,
                  context_instance=RequestContext(request))

@login_required
def change_attendance(request, event_id):
    event = Event.objects.get(id=event_id)
    attendance = Attendance.objects.filter(event=event, user=request.user)
    can_attend = request.GET.get('can_attend')
    if can_attend == 'x' and attendance:
        attendance[0].delete()
    else:
        can_attend = can_attend == '1'
        if attendance and (can_attend == '1') != attendance[0].can_attend:
            attendance[0].can_attend = can_attend
            attendance[0].save()
        elif not attendance:
            attendance = Attendance(user=request.user, event=event, can_attend=can_attend)
            attendance.save()

    return HttpResponseRedirect('/schedule/%s' % event_id)
