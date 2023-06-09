package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.AntoineParameter;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * AntoineSolidFunctionS8 class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class AntoineSolidFunctionS8 extends LevenbergMarquardtFunction {
    static Logger logger = LogManager.getLogger(AntoineSolidFunctionS8.class);

    /**
     * <p>
     * Constructor for AntoineSolidFunctionS8.
     * </p>
     */
    public AntoineSolidFunctionS8() {
        params = new double[2];
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.init(0);
        try {
            system.getPhase(0).getComponent(0).getSolidVaporPressure(dependentValues[0]);
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        return system.getPhase(0).getComponent(0).getSolidVaporPressure(dependentValues[0]);
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        if (i == 0) {
            system.getPhases()[0].getComponents()[0].setAntoineASolid(value);
        }
        if (i == 1) {
            system.getPhases()[0].getComponents()[0].setAntoineBSolid(value);
        }
        if (i == 2) {
            system.getPhases()[0].getComponents()[0].setAntoineCSolid(value);
        }
    }
}
