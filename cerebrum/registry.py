
class DashboardPluginRegistry(dict):
    def register(self, app_name, func):
        if app_name not in self:
            self[app_name] = func

    def unregister(self, app_name, func):
        if app_name in self:
            del self[app_name]


registry = DashboardPluginRegistry()
register = registry.register
unregister = registry.unregister
