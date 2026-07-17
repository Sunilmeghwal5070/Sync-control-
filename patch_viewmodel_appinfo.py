import re
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """                        newApp.copy(isLocked = existing.isLocked, isHidden = existing.isHidden)"""
replacement = """                        newApp.copy(isLocked = existing.isLocked, isHidden = existing.isHidden, notificationsEnabled = existing.notificationsEnabled)"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
