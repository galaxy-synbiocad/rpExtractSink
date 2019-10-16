# Galaxy rpCofactors

Galaxy tool that reads the output of RP2paths (link to the project), parses it, and adds the missing cofactors from mono-component reactions compared with the original reactions from wich the reaction rule is generated from. The output of the tool is a tar.xz file with each generated pathways (and sub-pathways) generated into an individual SBML files. 

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

### Prerequisites

* Docker - [Install](https://docs.docker.com/v17.09/engine/installation/)
* libSBML - [Anaconda library](https://anaconda.org/SBMLTeam/python-libsbml)

### Installing

Create a new section in the Galaxy tool_conf.xml from the config file:

```
<section id="retro" name="Retro Nodes">
  <tool file="/local/path/wrap_rpCofactors.xml" />
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
docker build -t brsynth/rp2reader .
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
    <tool id="rpCofactors" destination="docker_local" />
```

Finally, make sure that you give the python scripts execution permission:

```
chmod 755 *.py
```

## Running the tests

TODO

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Galaxy](https://galaxyproject.org) - The Galaxy project

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

TODO

## Authors

* **Melchior du Lac** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson
