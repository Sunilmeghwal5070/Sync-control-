#!/bin/bash
sed -i '/suspend fun updateConfig/i\
    suspend fun verifyConfigExists(pairCode: String): Boolean {\
        val snapshot = db.collection("devices").document(pairCode).get().await()\
        return snapshot.exists()\
    }\
' app/src/main/java/com/example/data/FirebaseRepository.kt
