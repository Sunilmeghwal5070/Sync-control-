with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun sendNotification(appName: String, content: String) {
        val currentDevice = allPairedDevices.value.firstOrNull { it.role == "child" }
        if (currentDevice != null && currentDevice.isConnected) {
            viewModelScope.launch {
                val log = NotificationLog(appName = appName, content = content, timestamp = System.currentTimeMillis())
                firebaseRepository.sendNotification(currentDevice.pairCode, log)
            }
        }
    }"""
replacement = """    fun sendNotification(appName: String, content: String) {
        val currentDevice = allPairedDevices.value.firstOrNull { it.role == "child" }
        if (currentDevice != null && currentDevice.isConnected) {
            val appInfo = _deviceConfig.value.installedApps.find { it.appName.equals(appName, ignoreCase = true) || it.packageName == appName }
            if (appInfo != null && !appInfo.notificationsEnabled) {
                // Notifications for this app are disabled by the parent/child
                return
            }
            viewModelScope.launch {
                val log = NotificationLog(appName = appName, content = content, timestamp = System.currentTimeMillis())
                firebaseRepository.sendNotification(currentDevice.pairCode, log)
            }
        }
    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
