package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.acentricFactorFitting;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * AcentricFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class AcentricFunction extends LevenbergMarquardtFunction {
    static Logger logger = LogManager.getLogger(AcentricFunction.class);

    /**
     * <p>
     * Constructor for AcentricFunction.
     * </p>
     */
    public AcentricFunction() {
        params = new double[1];
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.setTemperature(dependentValues[0]);
        system.init(0);
        system.init(1);
        try {
            thermoOps.bubblePointPressureFlash(false);
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        return Math.log(system.getPressure());
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        system.getPhases()[0].getComponents()[i].setAcentricFactor(value);
        system.getPhases()[1].getComponents()[i].setAcentricFactor(value);
    }
}
