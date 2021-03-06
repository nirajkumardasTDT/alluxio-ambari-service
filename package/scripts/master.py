#import status properties defined in -env.xml file from status_params class
import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call
import cPickle as pickle

class Master(Script):

  #Call setup.sh to install the service
  def install(self, env):
  
    import params
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    # Create the base_dir/alluxio dir
    cmd = '/bin/mkdir' + ' -p ' + params.base_dir 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    #extract archive and symlink dirs
    cmd = '/bin/tar' + ' -zxf ' + params.alluxio_package_dir + 'files/' +  params.alluxio_archive_file + ' --strip 1 -C ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    cmd = '/bin/ln' + ' -s ' + params.base_dir + ' ' + params.usr_base + 'current/alluxio'
    Execute('echo "Running ' + cmd + '"')
    try:
      Execute(cmd)
    except:
      pass

    self.configure(env)

  def configure(self, env):
    import params

    env.set_params(params)

    alluxio_config_dir = params.base_dir + '/conf/'
    alluxio_libexec_dir = params.base_dir + '/libexec/'

    File(format("{alluxio_config_dir}/alluxio-env.sh"),
          owner='root',
          group='root',
	  mode=0700,
          content=Template('alluxio-env.sh.template', conf_dir=alluxio_config_dir)
    )


  #Call start.sh to start the service
  def start(self, env):
    import params
    
    #call format
    cmd = params.base_dir + '/bin/alluxio ' + 'format'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
    
    #execute the startup script
    cmd = params.base_dir + '/bin/alluxio-start.sh ' + 'master'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
    
    # Create pid file - note check_process_status expects a SINGLE int in the file
    cmd = "mkdir -p " + params.pid_dir
    Execute(cmd)
    cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep AlluxioMaster | awk '{print $1}'`> " + params.pid_dir + "/AlluxioMaster.pid"
    Execute(cmd)
    pid_file = format("{params.pid_dir}/AlluxioMaster.pid")

  #Called to stop the service using alluxio provided stop
  def stop(self, env):
    import params
    
    #execure the startup script
    cmd = params.base_dir + '/bin/alluxio-stop.sh'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
    import params
    
    pid_file = format("{params.pid_dir}/AlluxioMaster.pid")
    check_process_status(pid_file)    

if __name__ == "__main__":
  Master().execute()
