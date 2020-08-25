from .model import get_model


def predict_churn(query):
    """
    This function classifies the array in input
    :param query: the logs to classify
    :return: the log related to churn
    """
    model = get_model()

    # use model to predict classification for query
    classification_results = model.predict(query)

    return classification_results
