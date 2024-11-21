from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CallRecord, Call

@receiver(post_save, sender=CallRecord)
def handle_call_record(sender, instance, created, **kwargs):
    if created:
        if instance.type == 'start':
            try:
                end_record = CallRecord.objects.get(call_id=instance.call_id, type='end')
                call = Call.objects.create(
                    call_record_start=instance,
                    call_record_end=end_record,
                    destination=instance.destination,
                    start_time=instance.timestamp,
                    duration=end_record.timestamp - instance.timestamp,
                )
                call.calculate_price()

                instance.processed = True
                end_record.processed = True
                instance.save(bypass_validation=True)
                end_record.save(bypass_validation=True)
            except CallRecord.DoesNotExist:
                pass
        elif instance.type == 'end':
            try:
                start_record = CallRecord.objects.get(call_id=instance.call_id, type='start')
                call = Call.objects.create(
                    call_record_start=start_record,
                    call_record_end=instance,
                    destination=start_record.destination,
                    start_time=start_record.timestamp,
                    duration=instance.timestamp - start_record.timestamp,
                )
                call.calculate_price()

                start_record.processed = True
                instance.processed = True
                start_record.save(bypass_validation=True)
                instance.save(bypass_validation=True)
            except CallRecord.DoesNotExist:
                pass
