package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.specificHeat;

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
import neqsim.util.database.NeqSimExperimentDatabase;

public class SpecificHeatCpFunctionTest {
    static Logger logger = LogManager.getLogger(SpecificHeatCpFunctionTest.class);

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
        NeqSimExperimentDatabase database = new NeqSimExperimentDatabase();

        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // BinaryFreezingPointData WHERE ComponentSolvent1='MEG' ORDER BY
        // FreezingTemperature");
        int i = 0;

        try (ResultSet dataSet = database.getResultSet(
                "SELECT * FROM PureComponentCpHeatCapacity WHERE ComponentName='seawater'")) {
            while (dataSet.next() && i < 4) {
                i++;
                SpecificHeatCpFunction function = new SpecificHeatCpFunction();
                double guess[] = {36.54003, -0.034802404, 0.0001168117, -1.3003096E-07}; // MEG
                function.setInitialGuess(guess);

                SystemInterface testSystem = new SystemSrkEos(280, 1.101);
                testSystem.addComponent(dataSet.getString("ComponentName"), 1.0);
                testSystem.setMixingRule(2);
                testSystem.init(0);
                testSystem.setTemperature(Double.parseDouble(dataSet.getString("Temperature")));
                testSystem.setPressure(5.0);
                double sample1[] = {testSystem.getPhase(0).getComponent(0).getz()};
                double standardDeviation1[] = {0.1, 0.1, 0.1};
                double val = Double.parseDouble(dataSet.getString("HeatCapacityCp"));

                SampleValue sample = new SampleValue(val, val / 100.0, sample1, standardDeviation1);
                sample.setFunction(function);
                sample.setReference(dataSet.getString("Reference"));
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }
        SampleSet sampleSet = new SampleSet(sampleList);
        optim.setSampleSet(sampleSet);

        optim.solve();
    }
}
