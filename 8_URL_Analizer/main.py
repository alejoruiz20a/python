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
    'Referrer-Policy': {
        'description': 'Controlar fuga de URLs Sensibles',
        'severity': 'MEDIUM',
        'recommendation': 'strict-origin-when-cross-origin',
        'min_score': 70
    },
    'Permissions-Policy': {
        'descaription': 'Limita el accesos a cámara/microfono/ubicación',
        'severity': 'LOW',
        'recommendations': 'geolocation=(), microphone=(), camera=()',
        'min_score': 70
    }
}

SEVERITY_WEIGHTS = {'CRITICAL': 30, 'HIGH': 25, 'MEDIUM': 15, 'LOW':10}

def evaluate_hsts(value):
    if not value or 'max-age' not in value.lower():
        return 0
    
    try:
        max_age = int(value.lower().split('max-age=')[1].split(';')[0].strip())
        score = 100 if max_age >= 31536000 else (70 if max_age>=15768000 else 40)
        return score
    except:
        return 20
    
def evaluate_csp(value):
    if not value:
        return 0
    
    dangerous = ['unsafe-inline', 'unsafe-eval', '*']
    return 40 if any(k in value.lower() for k in dangerous) else 100

def evaluate_xframe(value):
    if not value:
        return 0
    
    return 100 if any(x in value.lower() for x in ["deny", "sameorigin"]) else 30

def evaluate_xcontent(value):
    return 100 if value and "nosniff" in value.lower() else 0

def evaluate_referrer(value):
    if not value:
        return 0
    
    good = ["no-referrer", "same-origin", "strict-origin-when-cross-origin"]
    return 100 if any(p in value.lower() for p in good) else 50

def evaluate_permissions(value):
    return 100 if value else 0

EVALUATORS = {
    'Strict-Transport-Security': evaluate_hsts,
    'Content-Security-Policy': evaluate_csp,
    'X-Frame-Options': evaluate_xframe,
    'X-Content-Type-Options': evaluate_xcontent,
    'Referrer-Policy': evaluate_referrer,
    'Permissions-Policy': evaluate_permissions
}

class HTTPSecurityAnalyzer:
    def __init__(self):
        self.results = []

    def analyze_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            print("Analizando...")
            response = requests.get(url, timeout=15, allow_redirects=True)

            headers_data = {}
            for header_name, config in SECURITY_HEADERS.items():
                value = response.headers.get(header_name)
                evaluator = EVALUATORS.get(header_name)

                if evaluator:
                    score = evaluator(value)
                else:
                    score = 100 if value else 0

                headers_data[header_name] = {
                    'present': value is not None,
                    'value': value,
                    'score': score,
                    'severity': config['severity']
                }

            total_score = self._calculate_score(headers_data)
            grade = self._get_grade(total_score)

            result = {
                'url': url,
                'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                'status': response.status_code,
                'score': score,
                'grade': grade,
                'headers': headers_data
            }

            self.results.append(result)
            print(f"Completado! - {grade} ({total_score}/100)\n")
            return result
        
        except requests.exceptions.Timeout:
            print(f'Timeout: {url} tardó más de 15 segundos en responder.')
            return None
        except requests.exceptions.ConnectionError:
            print(f'Error en la conexión, no se pudo conectar a {url}')
            return None
        except requests.exceptions.TooManyRedirects:
            print('Demasiadas redirecciones.')
            return None
        except Exception as e:
            print(f'Error inesperado en {url}: {type(e).__name__} - {str(e)}\n')
            return None
        
    def _calculate_score(self, headers_data):
        total_weighted = 0
        total_weight = 0

        for data in headers_data.values():
            weight = SEVERITY_WEIGHTS.get(data['severity'], 10)
            total_weighted += data['score'] * weight
            total_weight += weight * 100

        return int((total_weighted/total_weight)*100) if total_weight > 0 else 0
    
    def _get_grade(self, score):
        if score>=90: return 'A'
        if score>=80: return 'B'
        if score>=70: return 'C'
        if score>=60: return 'D'
        return 'F'
    
# PRUEBA

prueba = HTTPSecurityAnalyzer()

prueba.analyze_url('https://www.youtube.com/')