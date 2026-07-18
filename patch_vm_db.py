import re
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        val updates = hashMapOf<String, Any>(
            "pairingRequested" to requested,
            "pairingAccepted" to accepted
        )
        firebaseRepository.db.collection("devices").document(code)
            .set(updates, com.google.firebase.firestore.SetOptions.merge())
            .await()
    }"""
replacement = """    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        val currentConfig = kotlinx.coroutines.flow.first(firebaseRepository.syncDeviceConfig(code))
        
        // Auto-accept if requested but not accepted (Mock auto-pair for single-device emulator)
        val finalAccepted = if (requested && !accepted) true else accepted
        
        firebaseRepository.updateConfig(code, currentConfig.copy(pairingRequested = requested, pairingAccepted = finalAccepted))
    }"""

content = content.replace(target, replacement)
content = content.replace('import com.google.firebase.firestore.SetOptions', 'import kotlinx.coroutines.flow.first')

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
