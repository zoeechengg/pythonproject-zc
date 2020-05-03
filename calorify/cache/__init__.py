import json

PREDICTION_NAMESPACE = "predictions"
NUTRITION_NAMESPACE = "foods_nutrition"

CACHE_NAMESPACES = [PREDICTION_NAMESPACE, NUTRITION_NAMESPACE]


class Cache:
    """
    A class for caching Clarifai image prediction results and EDAMAM nutritional information.
    """
    __cache__ = {}

    def __init__(self):
        """
        Creates the cache class and loads saved data from a local file.
        """
        with open('cache/cache.json', 'r') as f:
            self.__cache__ = json.load(f)
            for namespace in CACHE_NAMESPACES:
                if not self.__cache__.get(namespace):
                    self.__cache__[namespace] = {} # initialize a dict

    def persist(self):
        """
        Saves the cached data to a local file.
        """
        with open('cache/cache.json', 'w') as f:
            json.dump(self.__cache__, f)

    def get(self, namespace, key):
        """
        Given a namespace and a key, fetches the value for the key in the cache.
        """
        return self.__cache__[namespace].get(key)

    def set(self, namespace, key, value):
        """
        Given a namespace and a key, sets the value for the key in the cache.
        """
        self.__cache__[namespace][key] = value

    def get_prediction(self, filepath):
        """
        Gets the prediction result for a filepath or URL.
        """
        return self.get(PREDICTION_NAMESPACE, filepath)

    def get_nutrition(self, food):
        """
        Gets the nutrition information for an ingredient.
        """
        return self.get(NUTRITION_NAMESPACE, food)

    def set_prediction(self, filepath, prediction):
        """
        Sets the prediction result for a filepath or URL.
        """
        return self.set(PREDICTION_NAMESPACE, filepath, prediction)

    def set_nutrition(self, food, nutrients):
        """
        Sets the nutrition information for an ingredient.
        """
        return self.set(NUTRITION_NAMESPACE, food, nutrients)


cache = Cache()
