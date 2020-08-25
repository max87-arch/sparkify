from pypmml import Model


def get_model(path_model="../models/bayes.pmml"):
    """
    The function returns the model
    :param path_model: path to model
    :return: Model
    """
    # load model
    model = Model.load(path_model)
    return model
