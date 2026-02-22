from bridge.app_controller import AppController

app = AppController()
devices = app.get_available_devices()

print(devices)