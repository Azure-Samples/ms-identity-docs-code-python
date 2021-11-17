from setuptools import setup

setup(
    name='msal-py-cli',
    version='0.0.2',
    url='https://github.com/Azure-Samples/ms-identity-docs-code-python/cli-access-protected-api',
    license='MIT',
    author='Microsoft Docs',
    description='This example shows MSAL for Python usage. It is used as the backing code for the docs tutorial located at https://docs.microsoft.com/...',
    keywords='msal msal-python',
    include_package_data=True,
    py_modules=['cli'],
    python_requires=">=3.8",
    platforms='any',
    install_requires=[
        'click~=8.0',
        'msal~=1.16'
    ],
    entry_points={
        'console_scripts': [
            'msal-py-cli = cli:main',
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3 :: Only'
    ]
)
