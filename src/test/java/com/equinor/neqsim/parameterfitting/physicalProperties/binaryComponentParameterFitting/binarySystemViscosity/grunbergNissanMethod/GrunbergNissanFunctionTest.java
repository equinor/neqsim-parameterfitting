package com.equinor.neqsim.parameterfitting.physicalProperties.binaryComponentParameterFitting.binarySystemViscosity.grunbergNissanMethod;

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

public class GrunbergNissanFunctionTest {
    static Logger logger = LogManager.getLogger(GrunbergNissanFunctionTest.class);

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
                        "SELECT * FROM binarysystemviscosity WHERE ComponentName1='TEG'")) {
            logger.info("adding....");
            while (dataSet.next()) {
                GrunbergNissanFunction function = new GrunbergNissanFunction();
                double guess[] = {0.001};
                function.setInitialGuess(guess);
                SystemInterface testSystem = new SystemSrkEos(280, 0.001);
                double x1 = Double.parseDouble(dataSet.getString("x1"));
                testSystem.addComponent("TEG", x1);
                testSystem.addComponent("water", Double.parseDouble(dataSet.getString("x2")));
                testSystem.createDatabase(true);
                testSystem.setPressure(Double.parseDouble(dataSet.getString("Pressure")));
                testSystem.setTemperature(Double.parseDouble(dataSet.getString("Temperature")));
                testSystem.init(0);
                testSystem.initPhysicalProperties();
                double sample1[] = {x1, testSystem.getTemperature()};
                double standardDeviation1[] = {0.1};
                SampleValue sample =
                        new SampleValue(Double.parseDouble(dataSet.getString("Viscosity")),
                                Double.parseDouble(dataSet.getString("StdDev")), sample1,
                                standardDeviation1);
                sample.setFunction(function);
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }

        // double sample1[] = {0.1};
        // for(int i=0;i<sampleList.size();i++){
        // logger.info("ans: " + ((SampleValue)sampleList.get(i)).getFunction().calcValue(sample1));
        // }

        SampleSet sampleSet = new SampleSet(sampleList);
        optim.setSampleSet(sampleSet);

        // do simulations
        optim.solve();
        // optim.runMonteCarloSimulation();
        optim.displayCurveFit();
        // optim.displayCurveFit();
        optim.writeToTextFile("c:/testFit.txt");
    }
}
