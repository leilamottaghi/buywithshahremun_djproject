from celery import shared_task

@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"



from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime ,timedelta
import pytz
from django.utils import timezone
from store.models import Order

@shared_task(bind=True)
def remove_expired_otp_codes(self):
    # expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    # OtpCode.objects.filter(created__lt=expired_time).delete()
    OtpCode.objects.update(code=123)




@shared_task(bind=True)
def order_status_test(self):
    now = timezone.now()
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(seconds=2)
    qs = Order.objects.filter(created__lt=expired_time, status='awaiting_payment')
    qs.update(status='stale')


# @shared_task(bind=True)
# def order_status(self):
#     now = timezone.now()
#     # seconds
#     today_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2)
#     today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999) - datetime.timedelta(days=2)
#     qs = Order.objects.filter(timestamp__gte=today_start, timestamp__lte=today_end, status='awaiting_payment')
#     qs.update(status='stale')
#     # for obj in qs:
#     #     obj.status = "stale"
#     #     obj.save()


