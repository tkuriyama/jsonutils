from setuptools import setup
setup(
    name="jsonutils",
    version="0.3.1",
    packages=['jsonutils', 'jsonutils.lws', 'jsonutils.jbro'],
    scripts=['jsonutils/bin/jbro'],

    tests_require=['pytest'],
    install_requires=[],
    package_data={},

    author='Taro Kuriyama',
    author_email='taro@tarokuriyama.com',
    description="JSON Utilities in Python",
    license='MIT'
)
