package com.equinor.neqsim.parameterfitting.physicalProperties.binaryComponentParameterFitting.diffusivity;

import java.sql.ResultSet;
import java.util.ArrayList;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.junit.jupiter.api.Test;
import neqsim.statistics.parameterFitting.SampleSet;
import neqsim.statistics.parameterFitting.SampleValue;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardt;
import neqsim.thermo.system.SystemInterface;
import neqsim.thermo.system.SystemSrkEos;
import neqsim.util.database.NeqSimDataBase;

public class DiffusivityFunctionTest {
    static Logger logger = LogManager.getLogger(DiffusivityFunctionTest.class);

    /**
     * <p>
     * main.
     * </p>
     *
     * @param args an array of {@link java.lang.String} objects
     */
    @Test
    public void main() {
        LevenbergMarquardt optim = new LevenbergMarquardt();
        ArrayList<SampleValue> sampleList = new ArrayList<SampleValue>();

        // inserting samples from database
        try (NeqSimDataBase database = new NeqSimDataBase();
                ResultSet dataSet = database.getResultSet(
                        "SELECT * FROM binaryliquiddiffusioncoefficientdata WHERE ComponentSolute='CO2' AND ComponentSolvent='water'")) {
            logger.info("adding....");
            while (dataSet.next()) {
                DiffusivityFunction function = new DiffusivityFunction();
                double[] guess = {0.001};
                function.setInitialGuess(guess);
                SystemInterface testSystem = new SystemSrkEos(280, 0.001);
                testSystem.addComponent(dataSet.getString("ComponentSolute"), 1.0e-10);
                testSystem.addComponent(dataSet.getString("ComponentSolvent"), 1.0);
                testSystem.createDatabase(true);
                testSystem.setPressure(Double.parseDouble(dataSet.getString("Pressure")));
                testSystem.setTemperature(Double.parseDouble(dataSet.getString("Temperature")));
                testSystem.init(0);
                testSystem.setPhysicalPropertyModel(4);
                testSystem.initPhysicalProperties();
                double[] sample1 = {testSystem.getTemperature()};
                double[] standardDeviation1 = {0.1};
                SampleValue sample = new SampleValue(
                        Double.parseDouble(dataSet.getString("DiffusionCoefficient")), 0.01,
                        sample1, standardDeviation1);
                sample.setFunction(function);
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }

        // double sample1[] = {0.1};
        // for(int i=0;i<sampleList.size();i++){
        // logger.info"ans: " + ((SampleValue)sampleList.get(i)).getFunction().calcValue(sample1));
        // }

        SampleSet sampleSet = new SampleSet(sampleList);
        optim.setSampleSet(sampleSet);

        // do simulations
        // optim.solve();
        // optim.runMonteCarloSimulation();
        // optim.displayGraph();
        // optim.writeToTextFile("c:/testFit.txt");
    }
}
