

class BaseApprentice:
    """
    Base class used for policy and evaluation predictors.
    """

    predictor = None

    def init_model(self, input_fv_size, pi_size):
        raise NotImplementedError("Please Implement this method")

    def train(self, X, Y_pi, Y_r):
        raise NotImplementedError("Please Implement this method")

    def pred_eval(self, X):
        raise NotImplementedError("Please Implement this method")

    def pred_prob(self, X):
        raise NotImplementedError("Please Implement this method")