package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.acentricFactorFitting;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * ClassicAcentricFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class ClassicAcentricFunction extends LevenbergMarquardtFunction {
    static Logger logger = LogManager.getLogger(ClassicAcentricFunction.class);

    /**
     * <p>
     * Constructor for ClassicAcentricFunction.
     * </p>
     */
    public ClassicAcentricFunction() {}

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.setTemperature(dependentValues[0]);
        system.setPressure(system.getPhases()[0].getComponents()[0]
                .getAntoineVaporPressure(dependentValues[0]));
        // System.out.println("dep val " + dependentValues[0]);
        // System.out.println("pres from antoine: " + system.getPressure());
        system.init(0);
        system.init(1);
        try {
            thermoOps.bubblePointPressureFlash(false);
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        // System.out.println("pres: " + system.getPressure());
        return Math.log(system.getPressure());
    }

    /** {@inheritDoc} */
    @Override
    public double calcTrueValue(double val) {
        return Math.exp(val);
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        system.getPhases()[0].getComponents()[i].setAcentricFactor(value);
        system.getPhases()[1].getComponents()[i].setAcentricFactor(value);
    }
}
