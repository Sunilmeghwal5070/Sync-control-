import re

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    suspend fun requestPairing(code: String): kotlinx.coroutines.flow.Flow<DeviceConfig?> = kotlinx.coroutines.flow.callbackFlow {
        val listener = firebaseRepository.db.collection("devices").document(code).addSnapshotListener { snapshot, error ->
            if (error != null) return@addSnapshotListener
            if (snapshot != null && snapshot.exists()) {
                val config = snapshot.toObject(DeviceConfig::class.java)
                trySend(config)
            } else {
                trySend(null)
            }
        }
        kotlinx.coroutines.channels.awaitClose { listener.remove() }
    }

    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        firebaseRepository.db.collection("devices").document(code)
            .update("pairingRequested", requested, "pairingAccepted", accepted)
            .kotlinx.coroutines.tasks.await()
    }

    suspend fun verifyPairCode(code: String): Boolean {"""

content = content.replace("    suspend fun verifyPairCode(code: String): Boolean {", replacement)

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
