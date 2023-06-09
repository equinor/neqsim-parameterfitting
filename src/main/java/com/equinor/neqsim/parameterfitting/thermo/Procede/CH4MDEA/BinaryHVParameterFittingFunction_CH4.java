package com.equinor.neqsim.parameterfitting.thermo.Procede.CH4MDEA;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;
import neqsim.thermo.mixingRule.HVmixingRuleInterface;
import neqsim.thermo.phase.PhaseEosInterface;

/**
 * <p>
 * BinaryHVParameterFittingFunction_CH4 class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class BinaryHVParameterFittingFunction_CH4 extends LevenbergMarquardtFunction {
    int type = 0;
    int phase = 0;
    static Logger logger = LogManager.getLogger(BinaryHVParameterFittingFunction_CH4.class);

    /**
     * <p>
     * Constructor for BinaryHVParameterFittingFunction_CH4.
     * </p>
     */
    public BinaryHVParameterFittingFunction_CH4() {}

    /**
     * <p>
     * Constructor for BinaryHVParameterFittingFunction_CH4.
     * </p>
     *
     * @param phase a int
     * @param type a int
     */
    public BinaryHVParameterFittingFunction_CH4(int phase, int type) {
        this.phase = phase;
        this.type = type;
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        try {
            thermoOps.bubblePointPressureFlash(false);
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        return system.getPressure();
    }

    /** {@inheritDoc} */
    @Override
    public double calcTrueValue(double val) {
        return val;
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;

        if (i == 0) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijParameter(0, 2, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijParameter(0, 2, value);
        }
        if (i == 1) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijParameter(2, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijParameter(2, 0, value);
        }

        if (i == 4) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHValphaParameter(0, 2, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHValphaParameter(0, 2, value);
        }

        if (i == 2) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijTParameter(0, 2, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijTParameter(0, 2, value);
        }
        if (i == 3) {
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[0]).getMixingRule())
                    .setHVDijTParameter(2, 0, value);
            ((HVmixingRuleInterface) ((PhaseEosInterface) system.getPhases()[1]).getMixingRule())
                    .setHVDijTParameter(2, 0, value);
        }

        // if (i==0){
        /*
         * ((PhaseEosInterface)system.getPhases()[0]).getMixingRule().
         * setBinaryInteractionParameter(0,2, value);
         * ((PhaseEosInterface)system.getPhases()[1]).getMixingRule().
         * setBinaryInteractionParameter(0,2, value);
         */
        // }
    }
}
