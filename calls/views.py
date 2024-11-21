from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import filters
from .models import CallRecord, Call
from .serializers import CallRecordSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend


class CallRecordViewSet(ModelViewSet):
    """recording the start and end of telephone calls"""
    queryset = CallRecord.objects.all()
    serializer_class = CallRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['call_id']
    search_fields = ['call_id', 'type', 'source']
    filterset_fields = ['type']


class PhoneBillViewSet(ViewSet):
    """Complete monthly telephone invoices with the total invoice amount and details of each call \
        including the value of each call on the invoice"""
    def list(self, request):
        phone_number = request.query_params.get("phone_number")
        period = request.query_params.get("period")

        if not phone_number:
            return Response(
                {"error": "Telephone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not period:
            now = datetime.now()
            first_day_this_month = datetime(now.year, now.month, 1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            period = last_day_last_month.strftime("%m/%Y")

        try:
            month, year = map(int, period.split("/"))
            start_date = datetime(year, month, 1)
            end_date = (start_date + timedelta(days=31)) - timedelta(seconds=1)
        except ValueError:
            return Response(
                {"error": "the required period must be in the format MM/YYYY."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtrar chamadas no período
        calls = Call.objects.filter(
            call_record_end__timestamp__range=(start_date, end_date),
            call_record_start__source=phone_number
        )

        if not calls.exists():
            return Response(
                {"message": f"No calls found for number {phone_number} in period {period}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        total_price = calls.aggregate(total=Sum('price'))['total'] or 0

        call_details = [
            {
                "destination": call.destination,
                "start_time": call.start_time,
                "duration": str(call.duration),
                "price": float(call.price),
            }
            for call in calls
        ]

        return Response(
            {
                "phone_number": phone_number,
                "period": period,
                "total_price": float(total_price),
                "calls": call_details,
            },
            status=status.HTTP_200_OK,
        )
