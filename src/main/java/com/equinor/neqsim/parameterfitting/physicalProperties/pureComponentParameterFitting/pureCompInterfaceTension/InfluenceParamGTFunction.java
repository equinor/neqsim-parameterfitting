package com.equinor.neqsim.parameterfitting.physicalProperties.pureComponentParameterFitting.pureCompInterfaceTension;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import neqsim.statistics.parameterFitting.nonLinearParameterFitting.LevenbergMarquardtFunction;

/**
 * <p>
 * InfluenceParamGTFunction class.
 * </p>
 *
 * @author Even Solbraa
 * @version $Id: $Id
 */
public class InfluenceParamGTFunction extends LevenbergMarquardtFunction {
  static Logger logger = LogManager.getLogger(InfluenceParamGTFunction.class);

  /**
   * <p>
   * Constructor for InfluenceParamGTFunction.
   * </p>
   */
  public InfluenceParamGTFunction() {
    params = new double[1];
  }

  /** {@inheritDoc} */
  @Override
  public double calcValue(double[] dependentValues) {
    system.init(3);
    try {
      thermoOps.bubblePointPressureFlash(false);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
    system.initPhysicalProperties();
    return system.getInterphaseProperties().getSurfaceTension(0, 1) * 1e3;
  }

  /** {@inheritDoc} */
  @Override
  public void setFittingParams(int i, double value) {
    params[i] = value;
    system.getPhases()[0].getComponent(0).setSurfTensInfluenceParam(i, value);
    system.getPhases()[1].getComponent(0).setSurfTensInfluenceParam(i, value);
  }
}
