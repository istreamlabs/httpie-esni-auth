from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-esni-auth',
    description='ESNI auth plugin for HTTPie.',
    long_description=open('README.md').read().strip(),
    version='1.0.0',
    author='Daniel G. Taylor',
    author_email='dtaylor@istreamplanet.com',
    license='Apache2',
    url='https://github.com/pd/httpie-esni-auth',
    download_url='https://github.com/pd/httpie-esni-auth',
    py_modules=['httpie_esni_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_esni_auth = httpie_esni_auth:EsniAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
