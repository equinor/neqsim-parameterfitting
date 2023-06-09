package com.equinor.neqsim.parameterfitting.thermo.binaryInteractionParameterFitting.HuronVidalParameterFitting;

import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;
import neqsim.thermo.mixingRule.HVmixingRuleInterface;
import neqsim.thermo.phase.PhaseEosInterface;

/**
 *
 * @author Even Solbraa
 */
abstract class WongSandlerFunction extends LevenbergMarquardtFunction {
    /**
     * <p>
     * Constructor for WongSandlerFunction.
     * </p>
     */
    public WongSandlerFunction() {}

    /** {@inheritDoc} */
    @Override
    public void setDatabaseParameters() {
        params = new double[5];
        params[0] = ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0])
                .getMixingRule()).getHVDijParameter(0, 1);
        params[1] = ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0])
                .getMixingRule()).getHVDijParameter(1, 0);
        params[2] = ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0])
                .getMixingRule()).getHVDijTParameter(0, 1);
        params[3] = ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0])
                .getMixingRule()).getHVDijTParameter(1, 0);
        params[4] = ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0])
                .getMixingRule()).getKijWongSandler(1, 0);
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
        if (i == 2) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijTParameter(0, 1, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijTParameter(0, 1, value);
        }
        if (i == 3) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijTParameter(1, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijTParameter(1, 0, value);
        }
        if (i == 4) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHValphaParameter(1, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHValphaParameter(1, 0, value);
        }
        if (i == 5) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setKijWongSandler(1, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setKijWongSandler(1, 0, value);
        }
    }
}
