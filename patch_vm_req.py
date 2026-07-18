import re
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    suspend fun requestPairing(code: String): kotlinx.coroutines.flow.Flow<DeviceConfig?> = kotlinx.coroutines.flow.callbackFlow {
        val listener = firebaseRepository.db.collection("devices").document(code).addSnapshotListener { snapshot, error ->
            if (error != null) return@addSnapshotListener
            if (snapshot != null && snapshot.exists()) {
                val config = snapshot.toObject(DeviceConfig::class.java)
                trySend(config)
            } else {
                trySend(null)
            }
        }
        awaitClose { listener.remove() }
    }"""
replacement = """    suspend fun requestPairing(code: String): kotlinx.coroutines.flow.Flow<DeviceConfig?> {
        return firebaseRepository.syncDeviceConfig(code)
    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
