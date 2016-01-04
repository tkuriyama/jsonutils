from setuptools import setup, find_packages
setup(
    name = "pytextutils",
    version = "0.1.3",
    packages = ['pytextutils', 'pytextutils.json'],
    scripts = [],

    tests_require = ['pytest'],
    install_requires = [],
    package_data = {},

    author = 'Taro Kuriyama',
    author_email = 'taro@tarokuriyama.com',
    description = "Python Text Utilities",
    license = 'MIT'
)
