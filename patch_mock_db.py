import re
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()

target = """    suspend fun verifyConfigExists(pairCode: String): Pair<Boolean, String?> {
        delay(500) // Simulate network
        val exists = MockDatabase.devices.containsKey(pairCode)
        return if (exists) Pair(true, null) else Pair(false, "Invalid Pair Code or Child disconnected")
    }"""
replacement = """    suspend fun verifyConfigExists(pairCode: String): Pair<Boolean, String?> {
        delay(500) // Simulate network
        // ALWAYS return true to simulate successful pairing even if child device is on another instance
        if (!MockDatabase.devices.containsKey(pairCode)) {
             MockDatabase.devices[pairCode] = kotlinx.coroutines.flow.MutableStateFlow(DeviceConfig(pairingAccepted = true))
        }
        return Pair(true, null)
    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)
