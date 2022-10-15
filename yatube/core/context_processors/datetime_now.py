from datetime import datetime


def get_date_now(request):
    date_now = datetime.now()
    return {
        'year_now': date_now.year,
        'month_now': date_now.month,
        'day_now': date_now.day,
    }


def get_time_now(request):
    time_now = datetime.now().time()
    return {
        'time_now': time_now,
    }
