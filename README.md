# rpExtractSink docker

* Docker image: [brsynth/rpextractsink-standalone](https://hub.docker.com/r/brsynth/rpextractsink-standalone)

Tool that takes for input an SBML file and uses the MIRIAM annotations of the chemical species within a given compartment to find their InChI structures. Performs FVA to remove dead end metabolites. The output is a CSV RetroPath2.0 friendly CSV file that can be used as sink input. 

## Input

Required:
* **-input_sbml**: (string) Path to the input SBML file

Addtional information:
* **-remove_dead_end**: (boolean, default: True) Perform FVA evaluation to remove dead end metabolites
* **-compartment_id'**: (string, default: MNXC3) Specify the compartment from which to extract the sink molecules. The default are for MetaNetX files

## Output

* **-output_sink**: (string) Path to the output csv file

## Installing

To compile the docker use the following command:

```
docker build -t brsynth/rpextractsink-rest:dev .
```

### Running the test

To run the test, run the following command:

```
python run.py
```

## Dependencies

* Base docker image: [brsynth/rpbase](https://hub.docker.com/r/brsynth/rpbase)
* Cache docker image: [brsynth/rpcache](https://hub.docker.com/r/brsynth/rpcache)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac** 
* Thomas Duigou

## License

[MIT](https://github.com/Galaxy-SynBioCAD/rpExtractSink/blob/master/LICENSE)

## Acknowledgments

* Joan Hérisson

### How to cite rpMakeSource?
