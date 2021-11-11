from setuptools import setup

setup(
    name='docs-ms-identity-py-clientcredential',
    version='0.0.1',
    url='https://github.com/Azure-Samples/ms-identity-docs-code-python/cli-access-protected-api',
    license='MIT',
    author='Microsoft Docs',
    description='This example shows MSAL for Python usage. It is used as the backing code for the docs tutorial located at https://docs.microsoft.com/...',
    include_package_data=True,
    py_modules=['cli'],
    platforms='any',
    
    install_requires=[
        'click~=8.0',
        'msal~=1.16'
    ],
    entry_points={
        'console_scripts': [
            'docs-ms-identity-py-clientcredential = cli:main',
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
