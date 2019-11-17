from secret_santa import app


def get_http_response(response):
    http_response = app.response_class(response=response.json_data,
                                       status=response.status_code,
                                       mimetype='application/json')
    return http_response


def get_html_response(html, status_code):
    http_response = app.response_class(response=html,
                                       status=status_code,
                                       mimetype='text/html')
    return http_response
