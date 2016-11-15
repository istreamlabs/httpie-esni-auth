"""
ESNI (SCTE224) auth plugin for HTTPie.
"""
import base64, hashlib, hmac, os

from datetime import datetime
from httpie.plugins import AuthPlugin

try:
    import urlparse
except ImportError:
    import urllib.parse

__version__ = '1.0.0'
__author__ = 'Daniel G. Taylor <dtaylor@istreamplanet.com'
__licence__ = 'MIT'

ALGORITHM = 'HMAC-SHA256'
SIGNED_HEADERS = 'content-type;date;host'
SCOPE = os.environ.get('ESNI_SCOPE', 'esni')
SERVICE_NAME = os.environ.get('ESNI_SERVICE_NAME', 'esni')

def signMessage(secret, msg):
    """Create an HMAC-SHA256 hex digest given a message and secret key."""
    return hmac.new(secret, msg.encode('utf-8'), hashlib.sha256).digest()

def getRequestHash(method, path, query, contentType, date, host, payloadHash):
    """Get a hex digest of the concatenated canonical request."""
    h = hashlib.sha256()
    h.update(method)
    h.update('\n')
    h.update(path)
    h.update('\n')
    h.update(query)
    h.update('\n')
    h.update('content-type:')
    h.update(contentType)
    h.update('\n')
    h.update('date:')
    h.update(date)
    h.update('\n')
    h.update('host:')
    h.update(host)
    h.update('\n')
    h.update(SIGNED_HEADERS)
    h.update('\n')
    h.update(payloadHash)
    return h.hexdigest()

def getSignature(secret, serviceName, date, requestHash):
    """Get the signature hex digest for a request."""
    signingKey = signMessage(secret, serviceName)

    h = hmac.new(signingKey, None, hashlib.sha256)
    h.update(ALGORITHM)
    h.update('\n')
    h.update(date)
    h.update('\n')
    h.update(SCOPE)
    h.update('\n')
    h.update(requestHash)
    return h.hexdigest()

def getAuthorization(accessKey, serviceName, signature):
    """Returns an HTTP authorization header string."""
    return ALGORITHM + ' ' \
        + 'Credential=' + accessKey + '/' + SCOPE + ',' \
        + 'SignedHeaders=' + SIGNED_HEADERS + ',' \
        + 'Signature=' + signature

def sha256sum(body):
    """Get a SHA256 digest from a string."""
    h = hashlib.sha256()
    if body:
        h.update(body)
    return h.hexdigest()

def signRequest(accessKey, secret, method, serviceName, path, query, contentType, date, host, payloadHash):
    """Sign a request and return the authorization header."""
    requestHash = getRequestHash(method, path, query, contentType, date, host, payloadHash)
    signature = getSignature(secret, serviceName, date, requestHash)
    if 'VERBOSE' in os.environ:
        print "date:", date
        print "payload_hash:", payloadHash
        print "request_hash:", requestHash
        print "signature:", signature
    authorization = getAuthorization(accessKey, serviceName, signature)
    return authorization

class EsniAuth:
    """
    Provides an ESNI request signer for HTTPie. When called, a given request
    is signed via the addition of an `Authorization` header.
    """
    def __init__(self, access_id, secret_key):
        self.access_id = access_id
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, r):
        method = r.method.upper()
        url = urlparse.urlparse(r.url)
        content_type = r.headers.get('content-type') or ''
        date = r.headers.get('date')

        if not date:
            date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            r.headers['Date'] = date

        if 'VERBOSE' in os.environ:
            print(self.access_id, self.secret_key, method, SERVICE_NAME,
                url.path, url.query, content_type, date, url.netloc,
                sha256sum(r.body))

        r.headers['Authorization'] = signRequest(
            self.access_id, self.secret_key, method, SERVICE_NAME,
            url.path, url.query, content_type, date, url.netloc,
            sha256sum(r.body)
        )

        return r

class EsniAuthPlugin(AuthPlugin):

    name = 'ESNI (SCTE224) auth'
    auth_type = 'esni'
    description = 'Sign requests using the ESNI authentication method'

    def get_auth(self, username=None, password=None):
        return EsniAuth(username, password)
