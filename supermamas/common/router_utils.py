from functools import wraps
from urllib.parse import urlparse, urljoin
from flask import request, url_for, abort
from flask_login import current_user

# from http://flask.pocoo.org/snippets/62/
# by Armin Ronacher
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view