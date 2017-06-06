# Nexus 3 URL generator

Nexus 2 has a [nifty REST API](http://www.sonatype.org/nexus/2015/08/13/using-the-rest-api-in-nexus-2/) that you can use to, among other things, get the latest version of a given maven artifact.

However, after wondering why it didn't work on my Nexus 3 server, it seems [the REST API isn't built yet for Nexus 3](https://groups.google.com/a/glists.sonatype.com/d/msg/nexus-users/_CxNZVFSWAs/H3MmEqTGCgAJ) (which wasn't documented as well as I'd like it to be).

From reading the notes of other people encountering the issue and other scripts people generated (and me being a control freak and someone looking to practice Python), I decided to write my own URL generator for maven artifacts.

## How to use

The script takes six parameters (unix style format):

+ `--groupid (-g)`
+ `--artifactid (-a)`
+ `--extension (-e)`
+ `--version (-v)`
+ `--classifier (-c)`
+ `--repositoryurl (-r)`

`repositoryurl` is the base url for the maven repository (e.g. `https://nexus.yourorg.com/repository/maven-releases`). If you browse to the artifact you wish to programmatically grab, the other five values can be pulled from the artifact info.

`version` can either be the actual version you'd like to download. It can also accept `latest` and `release`, which grabs the artifacts Nexus labels as the latest and the release (which may not be the artifact you want - numerous discussions elsewhere about this topic).

If these values are not specified, the script will use the value specified in nexusdefaults.yml.

The script assumes connectivity to the repository. Unless `latest` or `release` is specified, it will generate the complete URL but with some error text. If `latest` or `release` is specified, the script will error out in checking the maven-metadata.

## Examples

`./getnexusurl.py -v latest`

Grabs the URL for the last uploaded artifact, using the defaults set in nexusdefaults.py.

`curl -O (./getnexusurl.py -v 1.2.3-release -a Artifact.Sample -g SampleOrg)`

Grabs the URL with the specified parameters then downloads it in the local directory.

## Other info

Script tested on ubuntu and WSL w/ Python 2. Go ahead and use this script if you'd like. If you have any questions, email me at ted (dot) glomski (at) gmail (dot) com.