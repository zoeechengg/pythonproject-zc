import json

PREDICTION_NAMESPACE = "predictions"
NUTRITION_NAMESPACE = "foods_nutrition"

CACHE_NAMESPACES = [PREDICTION_NAMESPACE, NUTRITION_NAMESPACE]


class Cache:
    __cache__ = {}

    def __init__(self):
        with open('cache/cache.json', 'r') as f:
            self.__cache__ = json.load(f)
            for namespace in CACHE_NAMESPACES:
                if not self.__cache__.get(namespace):
                    self.__cache__[namespace] = {} # initialize a dict

    def persist(self):
        with open('cache/cache.json', 'w') as f:
            json.dump(self.__cache__, f)

    def get(self, namespace, key):
        return self.__cache__[namespace].get(key)

    def set(self, namespace, key, value):
        self.__cache__[namespace][key] = value

    def get_prediction(self, filepath):
        return self.get(PREDICTION_NAMESPACE, filepath)

    def get_nutrition(self, food):
        return self.get(NUTRITION_NAMESPACE, food)

    def set_prediction(self, filepath, prediction):
        return self.set(PREDICTION_NAMESPACE, filepath, prediction)

    def set_nutrition(self, food, nutrients):
        return self.set(NUTRITION_NAMESPACE, food, nutrients)


cache = Cache()
