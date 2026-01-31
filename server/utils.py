import re
import requests

def parse_and_categorize_unsub(header_value):
    """
    Parses List-Unsubscribe header and categorizes links into 
    'mailto' and 'web' (http/https).
    """
    results = {'mailto': None, 'url': None}
    if not header_value:
        return results

    # Extract all links within < > brackets
    links = re.findall(r'<(.*?)>', header_value)
    
    for link in links:
        link = link.strip()
        if link.lower().startswith('mailto:'):
            results['mailto'] = link
        elif link.lower().startswith(('http://', 'https://')):
            results['url'] = link
            
    return results

def trigger_one_click_unsubscribe(web_url, post_header_value="List-Unsubscribe=One-Click"):
    """
    Triggers an RFC 8058 one-click unsubscribe via a POST request.
    According to the RFC, the 'List-Unsubscribe-Post' value must be 
    sent as the POST body.
    """
    try:
        # RFC 8058 requires a POST request with the specific body
        response = requests.post(
            web_url, 
            data={'List-Unsubscribe': 'One-Click'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Unsubscribe request failed: {e}")
        return False