import requests
import pandas as pd
from datetime import datetime

SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'description': 'Fuerza HTTPS (previene man-in-the-middle)',
        'severity': 'HIGH',
        'recommendation': 'max-age=31536000',
        'min_score': 70
    },
    'Content-Security-Policy': {
        'description': 'Previene el XSS definiendo fuentes permitidas',
        'severity': 'CRITICAL',
        'recommendation': "defaul-src 'self'; script-src 'self'",
        'min_score': 70
    },
    'X-Frame-Options': {
        'description': 'Previene el clickjacking (embeber en iframes)',
        'severity': 'HIGH',
        'recommendation': 'DENY o SAMEORIGIN',
        'min_score': 70
    },
    'X-Content-Type-Options': {
        'description': 'Previene ataques MIME-sniffing',
        'severity': 'MEDIUM',
        'recommendation': 'nosniff',
        'min_score': 70
    },
}