from subprocess import call

class display:
    _display_on = 0
    _config_data = None
    
    def __init__(self, config_data):
        self._config_data = config_data

    def turn_display_off(self):
        self._display_on = 0
        call(self._config_data["turn_off_action"], shell=True)

    def turn_display_on(self):
        self._display_on = 1
        call(self._config_data["turn_on_action"], shell=True)

    def is_turn_on_condition(self, input_signal):
        return input_signal == 0 and self._display_on == 1

    def is_turn_off_condition(self, input_signal):
        return input_signal == 1 and self._display_on == 0
