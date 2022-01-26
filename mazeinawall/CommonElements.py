class CommonElements:
    __ACTIONS_VALUES = [0, 1, 2, 3]
    __ACTIONS_NAMES = ["up", "down", "right", "left"]

    @staticmethod
    def actions():
        return dict(zip(CommonElements.__ACTIONS_NAMES, CommonElements.__ACTIONS_VALUES))

    @staticmethod
    def items():
        return {"wall": 1, "agent": 2, "space": 0}

