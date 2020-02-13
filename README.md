# Galaxy rpExtractSink

REST service version. Tool that takes for input an SBML file, uses the MIRIAM annotations to extract the cross-references and finds the InChI structure. The output a CSV file that is RetroPath2.0 friendly input as a sink. 

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

### Prerequisites

* Docker - [Install](https://docs.docker.com/v17.09/engine/installation/)
* libSBML - [Anaconda library](https://anaconda.org/SBMLTeam/python-libsbml)

### Installing

Create a new section in the Galaxy tool_conf.xml from the config file:

```
<section id="retro" name="Retro Nodes">
  <tool file="/local/path/wrap_rpExtractSink.xml" />
</section>
```

Make sure that docker can be run as root. It's important to run the docker as root user since it will be calling a script that writes files to a temporary folder inside the docker before sending back to Galaxy:

```
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
```

Build the docker image:

```
docker build -t brsynth/rpextractsink-rest .
docker run -p 8882:8888 brsynth/rpextractsink-rest
```

Make sure that the following entry exists under Galaxy's destination tag in job_conf.xml:

```
    <destination id="docker_local" runner="local">
      <param id="docker_enabled">true</param>
      <param id="docker_sudo">false</param>
      <param id="docker_auto_rm">true</param>
      <param id="docker_set_user">root</param>
    </destination>
```

And that the destination of the tool is refered under the tools tag of job_conf.xml:

```
    <tool id="rpExtractSink" destination="local" />
```

Finally, make sure that you give the python scripts execution permission:

```
chmod 755 *.py
```

## Running

TODO

### Example Input

TODO

## Deployment

TODO

## Built With

* [Galaxy](https://galaxyproject.org) - The Galaxy project

## Contributing

TODO

## Versioning

Version 0.1

## Authors

* **Melchior du Lac** 

## License

[MIT](https://github.com/Galaxy-SynBioCAD/rpExtractSink/blob/master/LICENSE)

## Acknowledgments

* Thomas Duigou
* Joan Hérisson
