package com.equinor.neqsim.parameterfitting.PVTsimulation;

import java.util.ArrayList;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.junit.jupiter.api.Test;
import neqsim.statistics.parameterFitting.SampleSet;
import neqsim.statistics.parameterFitting.SampleValue;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardt;
import neqsim.thermo.system.SystemInterface;
import neqsim.thermo.system.SystemSrkEos;

public class FunctionJohanSverdrupTest {
    static Logger logger = LogManager.getLogger(FunctionJohanSverdrupTest.class);

    /**
     * <p>
     * main.
     * </p>
     *
     * @param args an array of {@link java.lang.String} objects
     */
    @Test
    public void main() {
        ArrayList<SampleValue> sampleList = new ArrayList<SampleValue>();

        try {
            System.out.println("adding....");
            int i = 0;
            while (i < 1) {
                i++;

                SystemInterface tempSystem = new SystemSrkEos(273.15 + 83.5, 50.0);
                tempSystem.addComponent("nitrogen", 0.586);
                tempSystem.addComponent("CO2", 0.087);
                tempSystem.addComponent("methane", 17.0209);
                tempSystem.addComponent("ethane", 5.176);
                tempSystem.addComponent("propane", 6.652);
                tempSystem.addComponent("i-butane", 1.533);
                tempSystem.addComponent("n-butane", 3.544);
                tempSystem.addComponent("i-pentane", 1.585);
                tempSystem.addComponent("n-pentane", 2.036);
                tempSystem.addTBPfraction("C6", 2.879, 84.9 / 1000.0, 0.6668);
                tempSystem.addTBPfraction("C7", 4.435, 93.2 / 1000.0, 0.7243);
                tempSystem.addTBPfraction("C8", 4.815, 105.7 / 1000.0, 0.7527);
                tempSystem.addTBPfraction("C9", 3.488, 119.8 / 1000.0, 0.7743);
                tempSystem.addPlusFraction("C10", 45.944, 320.0 / 1000.0, 0.924);
                tempSystem.getCharacterization().characterisePlusFraction();
                tempSystem.createDatabase(true);
                tempSystem.setMixingRule(2);
                tempSystem.init(0);
                tempSystem.init(1);

                double[] sample1 = {273.15 + 100};
                double satPres = 75.0;
                double[] standardDeviation1 = {75.0 / 100.0};
                SampleValue sample =
                        new SampleValue(satPres, satPres / 100.0, sample1, standardDeviation1);
                FunctionJohanSverdrup function = new FunctionJohanSverdrup();
                double[] guess = {17.90};
                sample.setFunction(function);
                function.setInitialGuess(guess);
                sample.setThermodynamicSystem(tempSystem);
                sampleList.add(sample);
            }
        } catch (Exception ex) {
            logger.error("database error", ex);
        }

        SampleSet sampleSet = new SampleSet(sampleList);
        LevenbergMarquardt optim = new LevenbergMarquardt();
        optim.setMaxNumberOfIterations(8);
        optim.setSampleSet(sampleSet);
        optim.solve();
        optim.displayCurveFit();
    }
}
