import importlib


class Settings(object):
    def __init__(self):
        # 获取全局变量中的配置信息
        setting_modules = ['config.setting', 'config.api', 'config.usage']
        for setting_module in setting_modules:
            setting = importlib.import_module(setting_module)
            for attr in dir(setting):
                setattr(self, attr, getattr(setting, attr))

settings = Settings()
