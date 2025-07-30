from rest_framework import serializers
from .models import UrlCheck

class UrlCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlCheck
        fields = ['id', 'url', 'status_code', 'response_time', 
                 'is_reachable', 'error_message', 'checked_at', 'batch_id']
        read_only_fields = ['status_code', 'response_time', 'is_reachable', 
                           'error_message', 'checked_at', 'batch_id']

class UrlInputSerializer(serializers.Serializer):
    urls = serializers.ListField(
        child=serializers.URLField(),
        min_length=1,
        max_length=100
    )

class BatchStatusSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    success_rate = serializers.FloatField()