package com.equinor.neqsim.parameterfitting.thermo.binaryInteractionParameterFitting.EosInteractionParameterFitting;

import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;
import neqsim.thermo.mixingRule.HVmixingRuleInterface;
import neqsim.thermo.phase.PhaseEosInterface;

/**
 * <p>
 * CPAParameterFittingToSolubilityData_Vap class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class CPAParameterFittingToSolubilityData_Vap extends LevenbergMarquardtFunction {
    /**
     * <p>
     * Constructor for CPAParameterFittingToSolubilityData_Vap.
     * </p>
     */
    public CPAParameterFittingToSolubilityData_Vap() {
        params = new double[1];
    }

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        thermoOps.TPflash();
        // System.out.println("x " + system.getPhases()[1].getComponents()[0].getx());
        return system.getPhase(0).getComponent("water").getx() * 1.0e6; // lucia data
        // return system.getPhases()[1].getComponents()[0].getx(); // for MEG
    }

    /** {@inheritDoc} */
    @Override
    public void setFittingParams(int i, double value) {
        params[i] = value;
        if (i == 0) {
            ((PhaseEosInterface) system.getPhases()[0]).getMixingRule()
                    .setBinaryInteractionParameter(0, 1, value);
            ((PhaseEosInterface) system.getPhases()[1]).getMixingRule()
                    .setBinaryInteractionParameter(0, 1, value);
        }
        if (i == 2) {
            system.getPhases()[0].getComponents()[1].seta(value * 1e4);
            system.getPhases()[1].getComponents()[1].seta(value * 1e4);
        }
        if (i == 1) {
            system.getPhases()[0].getComponents()[1].setb(value);
            system.getPhases()[1].getComponents()[1].setb(value);
        }
        if (i == 3) {
            system.getPhase(0).getComponent(1).getAttractiveTerm().setm(value);
            system.getPhases()[1].getComponents()[1].getAttractiveTerm().setm(value);
        }
        if (i == 5) {
            system.getPhase(0).getComponent(1).setAssociationEnergy(value);
            system.getPhase(1).getComponent(1).setAssociationEnergy(value);
        }
        if (i == 4) {
            system.getPhase(0).getComponent(1).setAssociationVolume(value);
            system.getPhase(1).getComponent(1).setAssociationVolume(value);
        }
    }

    /**
     * <p>
     * setFittingParams2.
     * </p>
     *
     * @param i a int
     * @param value a double
     */
    public void setFittingParams2(int i, double value) {
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
    }
}
