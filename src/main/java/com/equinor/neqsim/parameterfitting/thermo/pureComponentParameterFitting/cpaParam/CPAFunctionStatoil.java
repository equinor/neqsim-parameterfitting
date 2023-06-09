package com.equinor.neqsim.parameterfitting.thermo.pureComponentParameterFitting.cpaParam;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * CPAFunctionStatoil class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class CPAFunctionStatoil extends LevenbergMarquardtFunction {
    static Logger logger = LogManager.getLogger(CPAFunctionStatoil.class);

    /**
     * <p>
     * Constructor for CPAFunctionStatoil.
     * </p>
     */
    public CPAFunctionStatoil() {}

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.setTemperature(dependentValues[0]);
        // system.init(0);
        // system.setPressure(system.getPhases()[0].getComponents()[0].getAntoineVaporPressure(dependentValues[0]));
        // System.out.println("pres from antoine: " + system.getPressure());
        try {
            thermoOps.bubblePointPressureFlash(false);
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        // System.out.println("pres: " + system.getPressure());
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
            system.getPhase(0).getComponent(0).getAttractiveTerm().setm(value);
            system.getPhases()[1].getComponents()[0].getAttractiveTerm().setm(value);
        }
        system.getPhases()[0].getComponents()[0].setMatiascopemanParams(i, value);
        system.getPhases()[1].getComponents()[0].setMatiascopemanParams(i, value);
        system.getPhases()[0].getComponents()[0].getAttractiveTerm().setParameters(i, value);
        system.getPhases()[1].getComponents()[0].getAttractiveTerm().setParameters(i, value);

        // value = 0.0;
        // for(int j=1;j<3;j++){
        // system.getPhases()[0].getComponents()[0].setSchwartzentruberParams(j, value);
        // system.getPhases()[1].getComponents()[0].setSchwartzentruberParams(j, value);
        // system.getPhases()[0].getComponents()[0].getAttractiveTerm().setParameters(j, value);
        // system.getPhases()[1].getComponents()[0].getAttractiveTerm().setParameters(j, value);
        // }
    }
}
