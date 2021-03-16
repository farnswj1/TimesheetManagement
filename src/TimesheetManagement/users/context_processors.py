from django.utils.timezone import now

def get_today_date(request):
    return {"today_date": now().today()}