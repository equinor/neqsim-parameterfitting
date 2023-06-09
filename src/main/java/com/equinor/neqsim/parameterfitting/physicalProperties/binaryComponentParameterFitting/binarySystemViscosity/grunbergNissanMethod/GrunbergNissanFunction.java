package com.equinor.neqsim.parameterfitting.physicalProperties.binaryComponentParameterFitting.binarySystemViscosity.grunbergNissanMethod;

import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * GrunbergNissanFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class GrunbergNissanFunction extends LevenbergMarquardtFunction {
    /**
     * <p>
     * Constructor for GrunbergNissanFunction.
     * </p>
     */
    public GrunbergNissanFunction() {}

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.init(1);
        system.initPhysicalProperties();
        return system.getPhases()[1].getPhysicalProperties().getViscosity() * 1e3;
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        // system.getPhases()[0].getPhysicalProperties().getMixingRule().setViscosityGij(value, 0,
        // 1);
        // system.getPhases()[0].getPhysicalProperties().getMixingRule().setViscosityGij(value, 1,
        // 0);
        system.getPhases()[1].getPhysicalProperties().getMixingRule().setViscosityGij(value, 1, 0);
        system.getPhase(1).getPhysicalProperties().getMixingRule().setViscosityGij(value, 0, 1);
    }
}
