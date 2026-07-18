import re

# Fix AppViewModel
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("kotlinx.coroutines.flow.first(firebaseRepository.syncDeviceConfig(code))", "firebaseRepository.syncDeviceConfig(code).first()")
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)

# Fix Service
with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'r') as f:
    content = f.read()

content = content.replace("kotlinx.coroutines.flow.first(firebaseRepository.syncDeviceConfig(childDevice.pairCode))", "firebaseRepository.syncDeviceConfig(childDevice.pairCode).first()")
with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'w') as f:
    f.write(content)

