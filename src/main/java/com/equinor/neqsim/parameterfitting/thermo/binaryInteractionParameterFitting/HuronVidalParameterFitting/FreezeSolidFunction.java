package com.equinor.neqsim.parameterfitting.thermo.binaryInteractionParameterFitting.HuronVidalParameterFitting;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * <p>
 * FreezeSolidFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class FreezeSolidFunction extends HuronVidalFunction {
    static Logger logger = LogManager.getLogger(FreezeSolidFunction.class);

    /**
     * <p>
     * Constructor for FreezeSolidFunction.
     * </p>
     */
    public FreezeSolidFunction() {}

    /** {@inheritDoc} */
    @Override
    public double calcValue(double[] dependentValues) {
        system.init(0);
        try {
            thermoOps.freezingPointTemperatureFlash();
        } catch (Exception ex) {
            logger.error(ex.getMessage(), ex);
        }
        return system.getTemperature();
    }
}
