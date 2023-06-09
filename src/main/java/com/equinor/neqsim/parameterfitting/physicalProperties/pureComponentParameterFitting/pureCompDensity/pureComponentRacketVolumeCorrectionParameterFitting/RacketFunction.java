package com.equinor.neqsim.parameterfitting.physicalProperties.pureComponentParameterFitting.pureCompDensity.pureComponentRacketVolumeCorrectionParameterFitting;

import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * RacketFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class RacketFunction extends LevenbergMarquardtFunction {
    /**
     * <p>
     * Constructor for RacketFunction.
     * </p>
     */
    public RacketFunction() {
        params = new double[1];
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.setTemperature(dependentValues[0]);
        system.init(1);
        system.initPhysicalProperties();
        return system.getPhases()[1].getPhysicalProperties().getDensity();
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        system.getPhases()[0].getComponents()[i].setRacketZ(value);
        system.getPhases()[1].getComponents()[i].setRacketZ(value);
    }
}
