package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.acentricFactorFitting;

import java.sql.ResultSet;
import java.util.ArrayList;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.junit.jupiter.api.Test;
import neqsim.statistics.parameterFitting.SampleSet;
import neqsim.statistics.parameterFitting.SampleValue;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardt;
import neqsim.thermo.system.SystemInterface;
import neqsim.thermo.system.SystemSrkTwuCoonParamEos;
import neqsim.util.database.NeqSimDataBase;

public class AcentricFunctionScwartzentruberTest {
    static Logger logger = LogManager.getLogger(AcentricFunctionScwartzentruberTest.class);

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
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='water' ORDER BY
        // Reference,Temperature");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='Piperazine'");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='MDEA' ORDER BY
        // Reference,Temperature");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='MEG' ORDER BY
        // Reference,Temperature");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='nitrogen' AND
        // VapourPressure<20");
        // ResultSet dataSet = database.getResultSet( "SELECT * FROM
        // PureComponentVapourPressures WHERE ComponentName='TEG' AND VapourPressure<0.5
        // ORDER BY Reference,Temperature");
        try (NeqSimDataBase database = new NeqSimDataBase()) {
            ResultSet dataSet = database.getResultSet(
                    "SELECT * FROM PureComponentVapourPressures WHERE ComponentName='mercury' AND VapourPressure<40 ORDER BY Reference,Temperature");

            while (dataSet.next()) {
                // AcentricFunctionScwartzentruber function = new
                // AcentricFunctionScwartzentruber();
                TwuCoon function = new TwuCoon();
                // MathiasCopeman function = new MathiasCopeman();
                // double guess[] = {0.0547834254, 0.0946785127, -2.2673294034}; // water
                // double guess[] = {0.00492, 0.00492, -0.00626}; // MDEA
                // double guess[] = {0.1662109957e-10, -11.5970369560e-10, 13.5388889636e-10};
                // // CO2
                // double guess[] ={0.0685841688, 0.9851816962, 4.2394590417} ; //mercury HYSYS
                // - Pc=1608bara

                double guess[] = {0.09245, 0.9784, 2.244};
                // double guess[] ={0.1208932305, 0.9580163852, 0.9875864928} ; //mercury PROII -
                // double guess[] = {0.4563609446}; //, -140.87783836,44.122}; // nitrogen
                function.setInitialGuess(guess);

                // SystemInterface testSystem = new SystemSrkSchwartzentruberEos(280, 0.101);
                SystemInterface testSystem = new SystemSrkTwuCoonParamEos(280, 0.01);
                // SystemInterface testSystem = new SystemPrEos1978(280, 0.01);
                // testSystem.setAttractiveTerm(13);
                testSystem.addComponent(dataSet.getString("ComponentName"), 100.0);
                // testSystem.createDatabase(true);
                double sample1[] = {Double.parseDouble(dataSet.getString("Temperature"))};
                double standardDeviation1[] = {0.1, 0.1, 0.1};
                double val = Math.log(Double.parseDouble(dataSet.getString("VapourPressure")));
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

        // do simulations
        // optim.solve();
        optim.runMonteCarloSimulation();
        optim.displayCurveFit();
        // optim.writeToTextFile("c:/testFit.txt");
    }
}
