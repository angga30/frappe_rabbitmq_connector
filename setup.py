from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="rabbitmq_connector",
	version=1.0,
	description="RabbitMQ Connector",
	author="angga prabuwisesa",
	author_email="angga@prabunesia.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
