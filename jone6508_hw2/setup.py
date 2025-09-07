from setuptools import find_packages, setup

package_name = 'jone6508_hw2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='joebn',
    maintainer_email='joebn@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'srv_server = jone6508_hw2.srv_server:main',
            'srv_client = jone6508_hw2.srv_client:main',
            'topic_pub  = jone6508_hw2.topic_pub:main',
            'topic_sub  = jone6508_hw2.topic_sub:main',
        ],
    },
)
