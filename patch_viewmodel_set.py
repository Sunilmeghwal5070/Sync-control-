import re
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        firebaseRepository.db.collection("devices").document(code)
            .update("pairingRequested", requested, "pairingAccepted", accepted)
            .await()
    }"""
replacement = """    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        val updates = hashMapOf<String, Any>(
            "pairingRequested" to requested,
            "pairingAccepted" to accepted
        )
        firebaseRepository.db.collection("devices").document(code)
            .set(updates, com.google.firebase.firestore.SetOptions.merge())
            .await()
    }"""
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
