import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target1 = """                                        viewModel.updateInstalledApps(updatedList)"""
replacement1 = """                                        viewModel.updateConfig(deviceConfig.copy(installedApps = updatedList))"""
content = content.replace(target1, replacement1)

target2 = """            onUpdateAppStatus = { updatedApps -> viewModel.updateInstalledApps(updatedApps) },"""
replacement2 = """            onUpdateAppStatus = { updatedApps -> viewModel.updateConfig(deviceConfig.copy(installedApps = updatedApps)) },"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
