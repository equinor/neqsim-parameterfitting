package com.equinor.neqsim.parameterfitting.thermo.binaryInteractionParameterFitting.HuronVidalParameterFitting;

import neqsim.thermo.mixingRule.HVmixingRuleInterface;
import neqsim.thermo.phase.PhaseEosInterface;

/**
 * <p>
 * BinaryHVParameterFittingToEquilibriumData class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class BinaryHVParameterFittingToEquilibriumData extends HuronVidalFunction {
    /**
     * <p>
     * Constructor for BinaryHVParameterFittingToEquilibriumData.
     * </p>
     */
    public BinaryHVParameterFittingToEquilibriumData() {
        params = new double[2];
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        double calcK = 0;
        double expK = 0;
        expK = dependentValues[1] / dependentValues[0];

        system.init(0);
        system.getPhases()[1].getComponents()[0].setx(dependentValues[0]);
        system.getPhases()[1].getComponents()[1].setx(1.0 - dependentValues[0]);
        system.getPhases()[0].getComponents()[0].setx(dependentValues[1]);
        system.getPhases()[0].getComponents()[1].setx(1.0 - dependentValues[1]);
        system.init(1);
        system.getPhases()[0].getComponents()[0].setK(Math.exp(
                Math.log(system.getPhases()[1].getComponents()[0].getFugacityCoefficient()) - Math
                        .log(system.getPhases()[0].getComponents()[0].getFugacityCoefficient())));
        calcK = system.getPhases()[0].getComponents()[0].getK();

        double diff = expK - calcK;
        // System.out.println("diff: " + diff);
        return diff;
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;

        if (i == 0) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijParameter(0, 1, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijParameter(0, 1, value);
        }
        if (i == 1) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijParameter(1, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijParameter(1, 0, value);
        }
    }
}
