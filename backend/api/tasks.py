from typing import Dict, Optional, Union
import time
import socket
import logging
import json
import requests
from celery import shared_task
from django.core.cache import cache
from requests.exceptions import RequestException, SSLError, ConnectionError, Timeout, TooManyRedirects
from .models import UrlCheck

logger = logging.getLogger(__name__)

CACHE_TTL = 60 * 5  # 5 minutes cache

@shared_task(bind=True, max_retries=3)
def check_url_health(self, url_check_id: int) -> Dict[str, Union[str, bool, Optional[int], Optional[float]]]:
    """
    Check the health of a URL and store the results.
    Uses Redis cache to avoid checking the same URL too frequently.
    
    Args:
        url_check_id: ID of the UrlCheck record to process
        
    Returns:
        Dict containing the check results with url, status, is_reachable,
        status_code, response_time and error_message
    """
    try:
        url_check = UrlCheck.objects.get(id=url_check_id)
        
        # Check cache first
        cache_key = f"url_health_{url_check.url}"
        cached_result = cache.get(cache_key)
        if cached_result:
            # Update DB with cached result but return immediately
            for key, value in cached_result.items():
                setattr(url_check, key, value)
            url_check.save()
            return {
                'url': url_check.url,
                'status': 'success' if url_check.is_reachable else 'failed',
                'is_reachable': url_check.is_reachable,
                'status_code': url_check.status_code,
                'response_time': url_check.response_time,
                'error_message': url_check.error_message,
                'cached': True
            }

        start_time = time.time()
        
        try:
            response = requests.get(
                url_check.url,
                timeout=30,
                allow_redirects=True
            )
            
            url_check.status_code = response.status_code
            url_check.response_time = time.time() - start_time
            url_check.is_reachable = response.status_code < 400
            url_check.error_message = ''
            
        except Timeout:
            url_check.is_reachable = False
            url_check.error_message = 'Request timed out'
        except SSLError:
            url_check.is_reachable = False
            url_check.error_message = 'SSL Certificate Error'
        except ConnectionError as e:
            url_check.is_reachable = False
            if isinstance(e.args[0], requests.packages.urllib3.exceptions.MaxRetryError):
                if isinstance(e.args[0].reason, socket.gaierror):
                    url_check.error_message = 'Domain does not exist'
                elif isinstance(e.args[0].reason, ConnectionRefusedError):
                    url_check.error_message = 'Connection refused'
                else:
                    url_check.error_message = 'Failed to establish connection'
        except TooManyRedirects:
            url_check.is_reachable = False
            url_check.error_message = 'Too many redirects'
        except RequestException:
            url_check.is_reachable = False
            url_check.error_message = 'Request failed'
        except Exception as e:
            url_check.is_reachable = False
            url_check.error_message = 'An unexpected error occurred'
            self.retry(exc=e, countdown=2 ** self.request.retries)
            return

        # Cache successful results
        if url_check.is_reachable:
            cache_data = {
                'status_code': url_check.status_code,
                'response_time': url_check.response_time,
                'is_reachable': url_check.is_reachable,
                'error_message': url_check.error_message
            }
            cache.set(cache_key, cache_data, CACHE_TTL)

        url_check.save()
        return {
            'url': url_check.url,
            'status': 'success' if url_check.is_reachable else 'failed',
            'is_reachable': url_check.is_reachable,
            'status_code': url_check.status_code,
            'response_time': url_check.response_time,
            'error_message': url_check.error_message,
            'cached': False
        }
        
    except UrlCheck.DoesNotExist:
        return {
            'status': 'error',
            'message': f'UrlCheck with id {url_check_id} not found'
        }
    except Exception as e:
        self.retry(exc=e, countdown=2 ** self.request.retries)