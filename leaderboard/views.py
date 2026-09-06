from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tests_app.models import Assignment
from django.db.models import Sum


@login_required
def leaderboard_view(request):
    # Overall leaderboard: total score across all completed tests, grouped by candidate
    assignments = Assignment.objects.filter(is_completed=True).select_related('candidate', 'test')

    leaderboard_data = {}
    for a in assignments:
        candidate = a.candidate
        if candidate.id not in leaderboard_data:
            leaderboard_data[candidate.id] = {
                'candidate': candidate,
                'total_score': 0,
                'total_max': 0,
                'tests_taken': 0,
            }
        leaderboard_data[candidate.id]['total_score'] += a.total_score
        leaderboard_data[candidate.id]['total_max'] += a.max_score
        leaderboard_data[candidate.id]['tests_taken'] += 1

    ranking = sorted(leaderboard_data.values(), key=lambda x: x['total_score'], reverse=True)

    for idx, entry in enumerate(ranking, start=1):
        entry['rank'] = idx
        entry['percentage'] = round((entry['total_score'] / entry['total_max']) * 100, 1) if entry['total_max'] > 0 else 0

    return render(request, 'leaderboard/leaderboard.html', {'ranking': ranking})