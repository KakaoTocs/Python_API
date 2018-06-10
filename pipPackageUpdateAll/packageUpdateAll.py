
import pkg_resources
from subprocess import call

dists = [d for d in pkg_resources.working_set]
for dist in dists:
    packageInfo = '{0}'.format(dist)
    packageName = packageInfo.split(' ')[0]
    print(packageName)
    call("pip install --upgrade " + packageName, shell=True)

'''
import pip

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
'''
