with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    suspend fun verifyPairCode(code: String): Boolean {
        return try {
            val snapshot = firebaseRepository.verifyConfigExists(code)
            snapshot
        } catch (e: Exception) {
            false
        }
    }"""
replacement = """    suspend fun verifyPairCode(code: String): Boolean {
        return try {
            val snapshot = firebaseRepository.verifyConfigExists(code)
            snapshot
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "verifyPairCode error", e)
            false
        }
    }"""
content = content.replace(target, replacement)

target2 = """    suspend fun initDeviceConfig(code: String) {
        firebaseRepository.updateConfig(code, DeviceConfig())
    }"""
replacement2 = """    suspend fun initDeviceConfig(code: String) {
        try {
            firebaseRepository.updateConfig(code, DeviceConfig())
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "initDeviceConfig error", e)
        }
    }"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
