from setuptools import setup, find_packages

setup(
    name='drone_teaching_package',         # Name of your package
    version='0.1.0',                       # Version number
    description='A package for teaching easytello and drone simulation commands',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Bhavya Bipin Gada',                    # Your name
    author_email='bgada1@umbc.edu', # Your email
    url='https://github.com/',    # URL of your project (GitHub, etc.)
    packages=find_packages(),              # Finds all packages (e.g., `drone_teaching_package`)
    install_requires=[                     # Dependencies
        'easytello',
        'DroneBlocksTelloSimulator'
    ],
    classifiers=[                          # Additional metadata
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',               # Minimum Python version requirement
)
