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
        'description': 'Limita el accesos a cámara/microfono/ubicación',
        'severity': 'LOW',
        'recommendation': 'geolocation=(), microphone=(), camera=()',
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

                print(evaluator)

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
                'score': total_score,
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

    def print_summary(self):
        if not self.results:
            print("\nNo hay resultados\n")
            return
        
        print("\n"+"="*90)
        print(" RESUMEN DEL ANÁLISIS ")
        print("="*90+"\n")

        for idx, r in enumerate(self.results, 1):
            print(f"==== [{idx}] {r['url']}")
            print(f"|    {r['grade']} ({r['score']}/100) | {r['timestamp']}")

            present = [(n, d['score']) for n, d in r['headers'].items() if d['present'] and d['score']>=70]
            weak = [(n, d['score']) for n, d in r['headers'].items() if d['present'] and d['score']<70]
            absent = [(n, d['score']) for n, d in r['headers'].items() if not d['present']]

            if present:
                print("|    Correctos:", ", ".join(f"{n}({s})" for n, s in present))
            if weak:
                print("|    Débiles:", ", ".join(f"{n}({s})" for n, s in weak))
            if absent:
                print("|    Ausentes:", ", ".join(f"{n}({s})" for n, s in absent))

    def print_detailed(self):
        if not self.results:
            print("\nNo hay resultados\n")
            return
        
        print("\n"+"="*90)
        print(" RESUMEN DEL ANÁLISIS ")
        print("="*90+"\n")

        for idx, r in enumerate(self.results, 1):
            print(f"\n[{idx}] {r['url']} - {r['grade']} ({r['score']}/100)")
            print("-"*90)

            for name, data in r['headers'].items():
                config = SECURITY_HEADERS[name]
                print(f"\n{name} [{data['severity']}]")
                print(f"{config['description']}")

                if data['present']:
                    status = "GOOD" if data['score'] >= 70 else "CAUTION"
                    print(f"    {status} | Score: {data['score']}/100")
                    print(f"    {data['value']}")
                else:
                    print("    AUSENTE (0/100)")
                    print(f"    Recomendación: {config['recommendation']}")

            print("\n"+"="*90)

    def export_csv(self, filename="security_report.csv"):
        if not self.results:
            print("\nNo hay resultados\n")
            return
        
        rows = []
        for r in self.results:
            row = {
                    'URL': r['url'],
                    'Fecha': r['timestamp'],
                    'Puntuación': r['score'],
                    'Calificación': r['grade'],
                   }
            for name, data in r['headers'].items():
                row[f"{name}_presente"] = "Sí" if data['present'] else "No"
                row[f"{name}_score"] = data['score']
            rows.append(row)

        pd.DataFrame(rows).to_csv(filename, index=False, encoding='utf-8')
        print(f"\nExportado: {filename}\n")


def main():
    analyzer = HTTPSecurityAnalyzer()

    print("\n"+"="*90)
    print(" ANALIZADOR DE SEGURIDAD HTTP ")
    print("="*90+"\n")

    while True:
        print("1. Analizar URLs")
        print("2. Ver Resumen")
        print("3. Ver detallado")
        print("4. Exportar CSV")
        print("5. Salir\n")

        choice = int(input("Opción: "))

        match choice:
            case 1:
                print("\nIngresa las URLs (línea vacía para terminar):\n")
                urls = []

                while True:
                    url = input("URL: ").strip()
                    if not url:
                        break
                    urls.append(url)

                if urls:
                    print(f"\nAnalizando {len(urls)} sitio(s)...")
                    for url in urls:
                        analyzer.analyze_url(url)
            case 2:
                analyzer.print_summary()
            case 3:
                analyzer.print_detailed()
            case 4:
                name= input("\nArchivo (Enter='security_report.csv): ").strip() or "security_report.csv"
                analyzer.export_csv(name if name.endswith('.csv') else name+'.csv')
            case 5:
                print('Cerrando analizador...')
            
            case _:
                print("Opción Invalida")
    
main()