from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Case, When, FloatField
from .models import UrlCheck
from .serializers import UrlCheckSerializer, UrlInputSerializer, BatchStatusSerializer
from .tasks import check_url_health
import uuid
import logging

logger = logging.getLogger(__name__)

class UrlCheckViewSet(viewsets.ModelViewSet):
    queryset = UrlCheck.objects.all()
    serializer_class = UrlCheckSerializer

    @action(detail=False, methods=['post'])
    def check_urls(self, request):
        """
        Endpoint to submit multiple URLs for health checking
        """
        serializer = UrlInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        batch_id = uuid.uuid4()
        url_checks = []
        
        # Create UrlCheck instances for each URL
        for url in serializer.validated_data['urls']:
            url_check = UrlCheck.objects.create(
                url=url,
                batch_id=batch_id
            )
            url_checks.append(url_check)
            
            # Launch Celery task for each URL
            try:
                logger.info(f"Sending task for URL: {url} with ID: {url_check.id}")
                task = check_url_health.delay(url_check.id)
                logger.info(f"Task sent successfully. Task ID: {task.id}")
            except Exception as e:
                logger.error(f"Error sending task: {str(e)}")
                url_check.error_message = f"Failed to queue task: {str(e)}"
                url_check.save()

        return Response({
            'batch_id': batch_id,
            'message': f'Processing {len(url_checks)} URLs',
            'urls': UrlCheckSerializer(url_checks, many=True).data
        }, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['get'])
    def batch_status(self, request):
        """
        Get the status of a batch of URL checks
        """
        batch_id = request.query_params.get('batch_id')
        if not batch_id:
            return Response(
                {'error': 'batch_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = UrlCheck.objects.filter(batch_id=batch_id)
        
        if not queryset.exists():
            return Response(
                {'error': 'Batch not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        stats = queryset.aggregate(
            total=Count('id'),
            completed=Count(Case(
                When(status_code__isnull=False, then=1),
                output_field=FloatField(),
            )),
        )
        
        stats['pending'] = stats['total'] - stats['completed']
        stats['success_rate'] = (
            queryset.filter(is_reachable=True).count() / stats['total']
            if stats['total'] > 0 else 0
        )

        serializer = BatchStatusSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def batch_results(self, request):
        """
        Get the results of a batch of URL checks
        """
        batch_id = request.query_params.get('batch_id')
        if not batch_id:
            return Response(
                {'error': 'batch_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = UrlCheck.objects.filter(batch_id=batch_id)
        
        if not queryset.exists():
            return Response(
                {'error': 'Batch not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UrlCheckSerializer(queryset, many=True)
        return Response(serializer.data)