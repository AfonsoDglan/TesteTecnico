from rest_framework import serializers
from .models import CallRecord


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = ['id', 'call_id', 'type', 'timestamp', 'source', 'destination']
        read_only_fields = ['id']

    def validate(self, data):
        if data['type'] == 'end' and (data.get('source') or data.get('destination')):
            raise serializers.ValidationError("End of call records cannot have 'source' or 'destination'.")
        if data['type'] == 'start' and (not data.get('source') or not data.get('destination')):
            raise serializers.ValidationError("Call start records must have 'source' and 'destination'.")
        return data
