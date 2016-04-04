OFF = 0
HEAT = 1
COOL = 2
FAN_ONLY = 3
UNKNOWN = -1


def print_state(state):
    states = {HEAT: "Heat", COOL: "Cool", FAN_ONLY: 'Fan Only', OFF: 'Off', UNKNOWN: 'Unknown'}

    return states.get(state, states[UNKNOWN])