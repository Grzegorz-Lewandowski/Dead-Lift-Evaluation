from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Analysis
from .serializers import AnalysisSerializer
from .services.analysis_service import run_deadlift_analysis


@api_view(['GET'])
def hello_world(request):
    return Response({
        'message': 'Hello World from Django API'
    })


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_analysis(request):
    serializer = AnalysisSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    analysis = serializer.save(status=Analysis.Status.PENDING)

    try:
        analysis.status = Analysis.Status.PROCESSING
        analysis.started_at = timezone.now()
        analysis.save(update_fields=['status', 'started_at'])

        result = run_deadlift_analysis(analysis.video.path)

        analysis.status = Analysis.Status.COMPLETED
        analysis.result = result
        analysis.completed_at = timezone.now()
        analysis.save(update_fields=['status', 'result', 'completed_at'])

    except Exception as exc:
        analysis.status = Analysis.Status.FAILED
        analysis.error_message = str(exc)
        analysis.completed_at = timezone.now()
        analysis.save(update_fields=['status', 'error_message', 'completed_at'])

    response_serializer = AnalysisSerializer(analysis)

    if analysis.status == Analysis.Status.FAILED:
        return Response(response_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_analysis(request, analysis_id):
    try:
        analysis = Analysis.objects.get(id=analysis_id)
    except Analysis.DoesNotExist:
        return Response(
            {'detail': 'Analysis not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AnalysisSerializer(analysis)
    return Response(serializer.data)