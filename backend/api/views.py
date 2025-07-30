from typing import List, Dict, Any
import uuid
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from .models import UrlCheck
from .tasks import check_url_health
from .serializers import UrlCheckSerializer, UrlListSerializer
from celery import group

class UrlCheckViewSet(viewsets.ModelViewSet):
    queryset = UrlCheck.objects.all()
    serializer_class = UrlCheckSerializer

    def _process_urls_chunk(self, urls: List[str], batch_id: str) -> List[Dict[str, Any]]:
        """Process a chunk of URLs and return their initial records"""
        url_checks = []
        for url in urls:
            url_check = UrlCheck.objects.create(
                url=url,
                batch_id=batch_id,
                is_reachable=False
            )
            url_checks.append({
                'id': url_check.id,
                'url': url,
                'status_code': None,
                'is_reachable': False,
                'error_message': '',
                'batch_id': batch_id
            })
            check_url_health.delay(url_check.id)
        return url_checks

    @action(detail=False, methods=['post'])
    def check_urls(self, request: Request) -> Response:
        """
        Check health for multiple URLs in parallel.
        URLs are processed in chunks for better performance.
        """
        serializer = UrlListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        urls = serializer.validated_data['urls']
        batch_id = str(uuid.uuid4())
        chunk_size = 10  # Process URLs in chunks of 10
        
        # Process URLs in chunks
        url_checks = []
        for i in range(0, len(urls), chunk_size):
            chunk = urls[i:i + chunk_size]
            url_checks.extend(self._process_urls_chunk(chunk, batch_id))

        return Response({
            'batch_id': batch_id,
            'urls': url_checks
        }, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['get'])
    def batch_status(self, request: Request) -> Response:
        """Get the status of a batch of URL checks"""
        batch_id = request.query_params.get('batch_id')
        if not batch_id:
            return Response(
                {'error': 'batch_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        total = UrlCheck.objects.filter(batch_id=batch_id).count()
        pending = UrlCheck.objects.filter(
            Q(batch_id=batch_id) & 
            (Q(status_code__isnull=True) & Q(error_message=''))
        ).count()

        return Response({
            'total': total,
            'pending': pending,
            'completed': total - pending
        })

    @action(detail=False, methods=['get'])
    def batch_results(self, request: Request) -> Response:
        """Get the results of a batch of URL checks"""
        batch_id = request.query_params.get('batch_id')
        if not batch_id:
            return Response(
                {'error': 'batch_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        url_checks = UrlCheck.objects.filter(batch_id=batch_id)
        serializer = UrlCheckSerializer(url_checks, many=True)
        return Response(serializer.data)