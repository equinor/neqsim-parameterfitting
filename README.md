# NeqSim experimental database and parameter fitting project
NeqSim experimental database and parameter fitting project.

Add experimental data in the [data folder](/data/) and make scripts for displaying, evaluating and updating models in the [example folder](/example/). In the [src folder](/src/) new models can be implemented for testing to the exerimental data.

An example for solubility data of CO2 in water is data put in the [data folder](/data/thermodynamics/VLE) and the evaluations put in the [example folder](/example/thermodynamics/VLE/).

See notebook on [how to work with the NeqSim parameter database](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/PVT/parameter_database.ipynb), and the description in the [neqsim wiki](https://github.com/equinor/neqsim/wiki/The-NeqSim-parameter-database).

## Setting up maven project
Call ```mvn validate``` to install the NeqSim core jar file located in resources folder to a local maven repository. Then the neqsim package shall be available for the java code. Try it out by calling ```mvn test```.
