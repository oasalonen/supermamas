
class ConfigurationService:
    __instance = None

    def __new__(cls, config=None):
        if not ConfigurationService.__instance:
            ConfigurationService.__instance = object.__new__(cls)
            ConfigurationService.__instance.config = config
        return ConfigurationService.__instance

    def get(self, name):
        return self.__instance.config.get(name)
