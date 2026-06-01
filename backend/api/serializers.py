import os

from rest_framework import serializers

from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    video_filename = serializers.SerializerMethodField()
    analysis_duration_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = [
            'id',
            'video',
            'video_filename',
            'status',
            'result',
            'error_message',
            'created_at',
            'started_at',
            'completed_at',
            'analysis_duration_seconds',
        ]
        read_only_fields = [
            'id',
            'video_filename',
            'status',
            'result',
            'error_message',
            'created_at',
            'started_at',
            'completed_at',
            'analysis_duration_seconds',
        ]

    def get_video_filename(self, obj):
        if not obj.video:
            return None

        return os.path.basename(obj.video.name)

    def get_analysis_duration_seconds(self, obj):
        if not obj.started_at or not obj.completed_at:
            return None

        duration = obj.completed_at - obj.started_at
        return round(duration.total_seconds(), 2)