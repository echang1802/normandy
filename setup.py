from setuptools import setup
setup(
    name='normandy',
    version='0.2',
    author='Eloy Chang',
    description='A data pipeline framework.',
    entry_points={
        'console_scripts': [
            'normandy=normandy:run',
            'normandy_create=normandy:start_project'
        ]
    }
)
