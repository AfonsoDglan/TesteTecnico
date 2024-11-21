from django.db import models


class CallRecord(models.Model):
    CALL_TYPE_CHOICES = [
        ('start', 'Início'),
        ('end', 'Fim'),
    ]

    call_id = models.CharField(max_length=50)
    type = models.CharField(max_length=5, choices=CALL_TYPE_CHOICES)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        constraints = [
            models.UniqueConstraint(fields=['call_id', 'type'], name='unique_call_record_type')
        ]
        indexes = [
            models.Index(fields=['call_id']),
        ]

    def __str__(self):
        return f"Call {self.call_id} - {self.get_type_display()} - {self.timestamp}"

    def save(self, *args, **kwargs):
        bypass_validation = kwargs.pop('bypass_validation', False)
        if not bypass_validation and self.processed and self.pk:
            raise ValueError("Registros processados não podem ser alterados.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.processed:
            if self.type == 'start':
                call = Call.objects.filter(call_record_start=self).first()
                if call:
                    related_record = call.call_record_end
                    call.delete()
            elif self.type == 'end':
                call = Call.objects.filter(call_record_end=self).first()
                if call:
                    related_record = call.call_record_start
                    call.delete()
            if related_record:
                related_record.processed = False
                related_record.save(bypass_validation=True)
        super().delete(*args, **kwargs)


class Call(models.Model):
    call_record_start = models.ForeignKey(CallRecord, related_name="start_record", on_delete=models.CASCADE)
    call_record_end = models.ForeignKey(CallRecord, related_name="end_record", on_delete=models.CASCADE)
    destination = models.CharField(max_length=11)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"call from {self.call_record_start.source} to {self.destination} - {self.start_time}"

    def calculate_duration(self):
        return self.call_record_end.timestamp - self.call_record_start.timestamp

    def calculate_price(self):
        start = self.call_record_start.timestamp
        duration = self.calculate_duration()

        # Taxas fixas
        fixed_rate = 0.36
        rate_per_minute = 0.09 if 6 <= start.hour < 22 else 0.00

        minutes = duration.total_seconds() // 60  # Minutos inteiros
        call_price = fixed_rate + (minutes * rate_per_minute)

        self.price = call_price
        self.save()

        return self.price
