#!/usr/bin/env python

import urllib2
import xml.etree.ElementTree as ET
import yaml
import sys
import getopt
import os

def parseopts(argv):
  helptext = 'valid parameters:\n --defaultsfile (-d, -f)\n --groupid (-g)\n --artifactid (-a)\n --extension (-e)\n --version (-v)\n --classifier (-c)\n --repositoryurl (-r)'
  try:
    opts, args = getopt.getopt(argv,"hg:a:e:v:c:r:d:f:",["defaultsfile","groupid=","artifactid=","extension=","version=","classifier=","repositoryurl="])
  except getopt.GetoptError:
    print helptext
    sys.exit(2)
  nexus_defaults_path = os.getcwd() + '/nexusdefaults.yml'
  for opt, arg in opts:
    if opt in ("--defaultsfile", "-d", "-f"):
      nexus_defaults_path = arg
  try:
    os.stat(nexus_defaults_path)
  except OSError:
    print ("file not found at " + nexus_defaults_path)
    sys.exit(2)
  with open(nexus_defaults_path, "r") as stream:
    output = yaml.load(stream)
  for opt, arg in opts:
    if opt == '-h':
      print helptext
      sys.exit()
    elif opt in ("--groupid", "-g"):
      output['groupid'] = arg
    elif opt in ("--artifactid", "-a"):
      output['artifactid'] = arg
    elif opt in ("--extension", "-e"):
      output['extension'] = arg
    elif opt in ("--version", "-v"):
      output['version'] = arg
    elif opt in ("--classifier", "-c"):
      output['classifier'] = arg
    elif opt in ("--repositoryurl", "-r"):
      output['repositoryurl'] = arg
  return output

def getnexusurl(**opts):
  metadata_url = opts['repositoryurl'] + '/' + opts['groupid'] + '/' + opts['artifactid'] + '/maven-metadata.xml'

  if opts['version'].lower() in ('latest','release'):
    try:
      xml = ET.fromstring(urllib2.urlopen(metadata_url).read())
    except (urllib2.URLError, urllib2.HTTPError):
      print ('Cannot open URL ' + metadata_url + ' - ensure this URL exists')
      sys.exit(2)
    version = xml.find('versioning').find(opts['version'].lower()).text
  else:
    version = opts['version']
  built_url = opts['repositoryurl'] + '/' + opts['groupid'] + '/' + opts['artifactid'] + '/' + version + '/' + opts['artifactid'] + '-' + version + '-' + opts['classifier'] + '.' + opts['extension']
  try:
    urllib2.urlopen(built_url)
  except (urllib2.URLError, urllib2.HTTPError):
    print ('Cannot open URL ' + built_url + ' - check your values and try again')
    sys.exit(2)
  return built_url

if __name__ == "__main__" :
  opts = parseopts(sys.argv[1:])
  print getnexusurl(**opts)
