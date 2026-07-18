import re
with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'r') as f:
    content = f.read()

target = """                    val configSnapshot = firebaseRepository.db.collection("devices").document(childDevice.pairCode).get().await()
                    if (configSnapshot.exists()) {
                        val config = configSnapshot.toObject(com.example.data.DeviceConfig::class.java)
                        if (config != null) {
                            val appInfo = config.installedApps.find { it.packageName == packageName }
                            if (appInfo != null && !appInfo.notificationsEnabled) {
                                return@launch
                            }
                        }
                    }"""
replacement = """                    val config = kotlinx.coroutines.flow.first(firebaseRepository.syncDeviceConfig(childDevice.pairCode))
                    if (config != null) {
                        val appInfo = config.installedApps.find { it.packageName == packageName }
                        if (appInfo != null && !appInfo.notificationsEnabled) {
                            return@launch
                        }
                    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'w') as f:
    f.write(content)
