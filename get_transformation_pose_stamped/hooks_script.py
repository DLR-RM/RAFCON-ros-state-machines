
def before_start(self, inputs, outputs, gvm, logger):
    """
    :param rafcon.statemachine.states.state self Is the root_state of the StateMachine the hook is used for
    :param dict inputs Dictionary of input-data-ports
    :param dict outputs Dictionary of output-data-ports
    :param rafcon.statemachine.global_variable_manager.GlobalVariableManager gvm Dictionary of input-data-ports
    :param logger: Logger to log messages to the debug-console.
    :return:
    """
    logger.debug("Start-before-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def after_start(self, inputs, outputs, gvm, logger):
    logger.debug("Start-after-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def finished(self, inputs, outputs, gvm, logger):
    logger.debug("Finished-hook function of root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def before_pause(self, inputs, outputs, gvm, logger):
    logger.debug("Pause-before-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def after_pause(self, inputs, outputs, gvm, logger):
    logger.debug("Pause-after-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def before_resume(self, inputs, outputs, gvm, logger):
    logger.debug("Resume-before-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def after_resume(self, inputs, outputs, gvm, logger):
    logger.debug("Resume-after-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def before_stop(self, inputs, outputs, gvm, logger):
    logger.debug("Stop-before-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))


def after_stop(self, inputs, outputs, gvm, logger):
    logger.debug("Stop-after-hook function root-state '{0}' {1} is run."
                 "".format(self.get_path(by_name=True), self.state_id))
