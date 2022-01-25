class CommonElements:
    __ACTIONS_VALUES = ["N", "S", "E", "W"]
    __ACTIONS_NAMES = ["up", "down", "right", "left"]

    @staticmethod
    def actions():
        return dict(zip(CommonElements.__ACTIONS_NAMES, CommonElements.__ACTIONS_VALUES))

    @staticmethod
    def items():
        return {"wall": 1, "agent": 2, "space": 0}

