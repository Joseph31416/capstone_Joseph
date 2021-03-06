class Validation:
    """
    Methods: set_params, check_desc, check_mode, check_group, check_payment_mode, check_all_input, check_routes
    Attributes: config, b1_desc, b2_desc, mode, group, payment_mode
    """

    def __init__(self, config):
        self.config = config
        self.b1_desc = None
        self.b2_desc = None
        self.mode = None
        self.group = None
        self.payment_mode = None

    def set_params(self, entry_dict):
        """
        :param entry_dict: input is a dictionaries containing required inputs
        :return: sets the values of the attributes based on the input
        """
        self.b1_desc = entry_dict.get("start", None)
        self.b2_desc = entry_dict.get("end", None)
        self.mode = entry_dict.get("mode", None)
        self.group = entry_dict.get("group", None)
        self.payment_mode = entry_dict.get("payment_mode", None)

    def __check_desc(self):
        """
        :return: checks if either the description of bus stop 1 or 2 is a NoneType
        """
        if self.b1_desc or self.b2_desc is None:
            return "Please choose another bus stop."
        return None

    def __check_mode(self):
        """
        :return: checks if mode is a NoneType and whether mode satisfies the presets
        """
        if self.mode is None:
            return "Please indicate whether you wish to sort the result by distance or fare."
        else:
            if self.mode.lower() not in self.config.MODE:
                return "Please enter a valid mode to sort by."
        return None

    def __check_group(self):
        """
        :return: checks if group is a NoneType and whether group satisfies the presets
        """
        if self.group is None:
            return "Please enter the payment group which you belong to."
        else:
            if self.group not in self.config.GROUP:
                return "PLease enter a valid payment group."
        return None

    def __check_payment_mode(self):
        """
        :return: checks if payment_mode is a NoneType and whether payment_mode satisfies the presets
        """
        if self.payment_mode is None:
            return "Please enter your mode of payment."
        else:
            if self.payment_mode not in self.config.PAYMENT_MODE:
                return "Please enter a valid mode of payment."
        return None

    def check_all_input(self):
        """
        :return: runs check on description, mode, group and payment_mode and returns the result
        """
        temp = [
            self.__check_desc(),
            self.__check_mode(),
            self.__check_group(),
            self.__check_payment_mode(),
            None
        ]
        if temp != [None]*5:
            passed = True
        else:
            passed = False
        return temp, passed

    @staticmethod
    def check_routes(bus_routes, b1, b2, err_msg):
        """
        :param bus_routes: a string indicating the bus route
        :param b1: description of bus stop 1
        :param b2: description of bus stop 2
        :param err_msg: existing list of error messages
        :return: returns an error message and the test result
        """
        passed = True
        if len(bus_routes) == 0:
            err = f"No direct bus between {b1} and {b2}."
            passed = False
            err_msg[4] = err
            return err_msg, passed
        return err_msg, passed
