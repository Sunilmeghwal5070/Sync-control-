import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """        ChildDashboard(
            pairCode = pairedDevice.pairCode,
            deviceConfig = deviceConfig,
            onSendMockNotification = { app, msg -> viewModel.sendNotification(app, msg) },
            onDisconnect = onDisconnect
        )"""
replacement = """        ChildDashboard(
            pairCode = pairedDevice.pairCode,
            deviceConfig = deviceConfig,
            onSendMockNotification = { app, msg -> viewModel.sendNotification(app, msg) },
            onUpdateAppStatus = { updatedApps -> viewModel.updateInstalledApps(updatedApps) },
            onDisconnect = onDisconnect
        )"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
