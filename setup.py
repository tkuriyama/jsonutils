from setuptools import setup
setup(
    name="jsonutils",
    version="0.1.6",
    packages=['jsonutils', 'jsonutils.lws', 'jsonutils.jbro'],
    scripts=['jbro/bin/jbro'],

    tests_require=['pytest'],
    install_requires=[],
    package_data={},

    author='Taro Kuriyama',
    author_email='taro@tarokuriyama.com',
    description="JSON Utilities in Python",
    license='MIT'
)
