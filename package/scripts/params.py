#!/usr/bin/config python
from resource_management import *
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.version import compare_versions, format_stack_version
from resource_management.libraries.functions.format import format

import commands
import os.path

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# identify archive file
alluxio_archive_file = config['configurations']['alluxio-env']['alluxio.archive.file']

# alluxio master address
alluxio_master = config['clusterHostInfo']['alluxio_master_hosts'] 

# alluxio underfs address
underfs_addr = config['configurations']['alluxio-env']['alluxio.underfs.address']

# alluxio worker memory alotment 
worker_mem = config['configurations']['alluxio-env']['alluxio.worker.memory']

# Find current stack and version to push agent files to
stack_name = default("/hostLevelParams/stack_name", None)
stack_version = format_stack_version(default("/commandParams/version", None))

# hadoop params
namenode_address = None
if 'dfs.namenode.rpc-address' in config['configurations']['hdfs-site']:
  namenode_rpcaddress = config['configurations']['hdfs-site']['dfs.namenode.rpc-address']
  namenode_address = format("hdfs://{namenode_rpcaddress}")
else:
  namenode_address = config['configurations']['core-site']['fs.defaultFS']



# Set install dir
cmd = "/usr/bin/hdp-select versions"
usr_base = "/usr/hdp/"
base_dir = usr_base + commands.getoutput(cmd) + "/alluxio/"
  
# Alluxio archive on agent nodes
alluxio_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version[:3] + "/services/ALLUXIO/package/"

# alluxio log dir
log_dir = config['configurations']['alluxio-env']['alluxio.log.dir']

# alluxio log dir
pid_dir = config['configurations']['alluxio-env']['alluxio.pid.dir']

