# rpExtractSink

Tool that takes for input an SBML file, uses the MIRIAM annotations to extract the cross-references and finds the InChI structure. The output a CSV file that is RetroPath2.0 friendly input as a sink. 

## Information Flow

### Input

Required information:
* Either tar.xz input collection of rpSBML files or a single rpSBML file.

Advanced options:
* Name of the heterologous pathway: (default: rp_pathway) Groups ID of the heterologous pathway
* IP address of the rpExtractSink REST service: IP address of the REST service

### Output

* Sink: The output is a CSV RetroPath2.0 friendly format 

## Installing

To compile the docker use the following command:

```
docker build -t brsynth/rpextractsink-rest .
```

To run the service as localhost, use the following command:

```
docker run -p 8882:8888 brsynth/rpextractsink-rest
```

### Prerequisites

* Docker - [Install](https://docs.docker.com/v17.09/engine/installation/)
* libSBML - [Anaconda library](https://anaconda.org/SBMLTeam/python-libsbml)

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

### How to cite rpMakeSource?

TODO
