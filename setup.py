from setuptools import setup
setup(
    name="jsonutils",
    version="0.1.5",
    packages=['jsonutils', 'jsonutils.lws'],
    scripts=[],

    tests_require=['pytest'],
    install_requires=[],
    package_data={},

    author='Taro Kuriyama',
    author_email='taro@tarokuriyama.com',
    description="JSON Utilities in Python",
    license='MIT'
)
