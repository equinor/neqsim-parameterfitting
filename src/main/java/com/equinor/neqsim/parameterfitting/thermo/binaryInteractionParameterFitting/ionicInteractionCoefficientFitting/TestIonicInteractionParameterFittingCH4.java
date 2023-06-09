package com.equinor.neqsim.parameterfitting.thermo.binaryInteractionParameterFitting.ionicInteractionCoefficientFitting;

import java.sql.ResultSet;
import java.util.ArrayList;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.SampleSet;
import neqsim.statistics.parameterFitting.SampleValue;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardt;
import neqsim.thermo.system.SystemFurstElectrolyteEos;
import neqsim.thermo.system.SystemInterface;
import neqsim.util.database.NeqSimDataBase;

/**
 * <p>
 * TestIonicInteractionParameterFittingCH4 class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class TestIonicInteractionParameterFittingCH4 {
    static Logger logger = LogManager.getLogger(TestIonicInteractionParameterFittingCH4.class);

    /**
     * <p>
     * main.
     * </p>
     *
     * @param args an array of {@link java.lang.String} objects
     */
    public static void main(String[] args) {
        LevenbergMarquardt optim = new LevenbergMarquardt();
        ArrayList<SampleValue> sampleList = new ArrayList<SampleValue>();

        // inserting samples from database
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // activityCoefficientTable WHERE Component1='MDEA' AND Component2='water'");AND
        // Reference='Lemoine2000'
        double guess[] = {-0.0001617266, 0.5 * 1e-3}; // , -0.0932324951}; //, 0.6465043774,};
        // -0,0001550096 0,0007612383

        // double guess[] = {-0.0000309356,-0.1469925592,-0.0272808384};

        try (NeqSimDataBase database = new NeqSimDataBase();
                ResultSet dataSet =
                        database.getResultSet("SELECT * FROM Co2Ch4MDEA WHERE loading<1.9"); // AND
                                                                                             // temperature=313.15
                                                                                             // AND
                                                                                             // pressure<210
                                                                                             // AND
                                                                                             // wt=30");
        ) {
            int i = 0;
            while (dataSet.next() && i < 100) {
                i++;
                IonicInteractionParameterFittingFunctionCH4 function =
                        new IonicInteractionParameterFittingFunctionCH4();

                SystemInterface testSystem = new SystemFurstElectrolyteEos((273.15 + 25.0), 100.0);
                testSystem.addComponent(dataSet.getString("gass2"),
                        Double.parseDouble(dataSet.getString("molCH4")));
                testSystem.addComponent(dataSet.getString("gass1"),
                        Double.parseDouble(dataSet.getString("molCO2")));
                testSystem.addComponent(dataSet.getString("liquid1"),
                        Double.parseDouble(dataSet.getString("molMDEA")));
                testSystem.addComponent(dataSet.getString("liquid2"),
                        Double.parseDouble(dataSet.getString("molWater")));

                double temperature = Double.parseDouble(dataSet.getString("Temperature"));
                double pressure = Double.parseDouble(dataSet.getString("Pressure"));
                testSystem.setPressure(pressure);
                testSystem.setTemperature(temperature);
                testSystem.chemicalReactionInit();
                // testSystem.createDatabase(true);
                testSystem.setMixingRule(4);
                testSystem.init(0);
                double sample1[] = {testSystem.getPhases()[0].getComponents()[0]
                        .getNumberOfMolesInPhase()
                        / testSystem.getPhases()[0].getComponents()[2].getNumberOfMolesInPhase()};
                double standardDeviation1[] = {0.01};

                SampleValue sample =
                        new SampleValue(pressure, pressure / 100.0, sample1, standardDeviation1);
                function.setInitialGuess(guess);
                sample.setFunction(function);
                sample.setReference("addicks");
                sample.setDescription(Double.toString(pressure));
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }
        // dataSet = database.getResultSet( "SELECT * FROM Co2Ch4MDEA WHERE loading<1.9
        // AND temperature<453.15 AND pressure<210 AND wt<70");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // activityCoefficientTable WHERE Component1='MDEA' AND Component2='water'");AND
        // Reference='Lemoine2000'

        try (NeqSimDataBase database = new NeqSimDataBase();
                ResultSet dataSet =
                        database.getResultSet("SELECT * FROM Co2Ch4MDEA WHERE loading<1.9")) // AND
        // temperature=313.15
        // AND
        // pressure<210
        // AND
        // wt=50");)
        {
            int i = 0;
            while (!dataSet.next() && i < 100) {
                i++;
                IonicInteractionParameterFittingFunctionCH4_1 function =
                        new IonicInteractionParameterFittingFunctionCH4_1();

                SystemInterface testSystem = new SystemFurstElectrolyteEos((273.15 + 25.0), 100.0);
                testSystem.addComponent(dataSet.getString("gass2"),
                        Double.parseDouble(dataSet.getString("molCH4")));
                testSystem.addComponent(dataSet.getString("gass1"),
                        Double.parseDouble(dataSet.getString("molCO2")));
                testSystem.addComponent(dataSet.getString("liquid1"),
                        Double.parseDouble(dataSet.getString("molMDEA")));
                testSystem.addComponent(dataSet.getString("liquid2"),
                        Double.parseDouble(dataSet.getString("molWater")));

                double temperature = Double.parseDouble(dataSet.getString("Temperature"));
                double pressure = Double.parseDouble(dataSet.getString("Pressure"));
                testSystem.setPressure(pressure);
                testSystem.setTemperature(temperature);
                testSystem.chemicalReactionInit();
                // testSystem.createDatabase(true);
                testSystem.setMixingRule(4);
                testSystem.init(0);
                double sample1[] = {testSystem.getPhases()[0].getComponents()[1]
                        .getNumberOfMolesInPhase()
                        / testSystem.getPhases()[0].getComponents()[2].getNumberOfMolesInPhase()};
                double standardDeviation1[] = {0.01};
                double y1 = Double.parseDouble(dataSet.getString("y1"));
                SampleValue sample = new SampleValue(pressure * y1, y1 * pressure / 100.0, sample1,
                        standardDeviation1);
                function.setInitialGuess(guess);
                sample.setFunction(function);
                sample.setReference("addicks");
                sample.setDescription(Double.toString(pressure));
                sample.setThermodynamicSystem(testSystem);
                sampleList.add(sample);
            }
        } catch (

        Exception ex) {
            logger.error("database error", ex);
        }
        SampleSet sampleSet = new SampleSet(sampleList);
        optim.setSampleSet(sampleSet);

        // do simulations

        optim.solve();
        // optim.runMonteCarloSimulation();
        // optim.displayCurveFit();
        // optim.displayGraph();
        optim.displayCurveFit();
        optim.writeToTextFile("c:/testFit.txt");
    }
}
