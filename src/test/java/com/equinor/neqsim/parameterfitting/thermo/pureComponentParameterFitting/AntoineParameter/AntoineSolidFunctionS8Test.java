package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.AntoineParameter;

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

public class AntoineSolidFunctionS8Test {
    static Logger logger = LogManager.getLogger(AntoineSolidFunctionS8Test.class);

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
        try (NeqSimDataBase database = new NeqSimDataBase()) {
            ResultSet dataSet = database.getResultSet(
                    "SELECT * FROM PureComponentVapourPressures WHERE ComponentName='S8' AND VapourPressure<100");

            while (dataSet.next()) {
                AntoineSolidFunctionS8 function = new AntoineSolidFunctionS8();
                // double guess[] = {8.046, -4600.0, -144.0}; // S8
                double guess[] = {1.181E1, -8.356E3}; // S8
                function.setInitialGuess(guess);

                SystemInterface testSystem = new SystemSrkEos(280, 0.001);
                testSystem.addComponent(dataSet.getString("ComponentName"), 100.0);

                double sample1[] = {Double.parseDouble(dataSet.getString("Temperature"))};
                double vappres = Double.parseDouble(dataSet.getString("VapourPressure"));
                double standardDeviation1[] = {0.15};
                SampleValue sample = new SampleValue(vappres,
                        Double.parseDouble(dataSet.getString("StandardDeviation")), sample1,
                        standardDeviation1);
                sample.setFunction(function);

                function.setInitialGuess(guess);
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }

        SampleSet sampleSet = new SampleSet(sampleList);
        optim.setSampleSet(sampleSet);

        // do simulations
        optim.solve();
        // optim.runMonteCarloSimulation();
        optim.displayCurveFit();
        // optim.writeToTextFile("c:/testFit.txt");
    }
}
