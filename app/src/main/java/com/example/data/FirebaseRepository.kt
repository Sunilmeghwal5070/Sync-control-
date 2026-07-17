package com.example.data

import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.ListenerRegistration
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await

data class DeviceConfig(
    val wifi: Boolean = false,
    val bluetooth: Boolean = false,
    val flashlight: Boolean = false,
    val hotspot: Boolean = false,
    val ringerMode: Int = 2, // 0 = silent, 1 = vibrate, 2 = normal
    val volume: Int = 50,
    val brightness: Int = 100,
    val lock: Boolean = false,
    val aeroplaneMode: Boolean = false,
    val screenshotRequested: Boolean = false,
    val batterySaver: Boolean = false,
    val dndMode: Boolean = false,
    val screenTimeout: Int = 30,
    val cameraAccess: Boolean = true,
    val microphoneAccess: Boolean = true,
    val batteryLevel: Int = 85,
    val location: LocationData = LocationData(0.0, 0.0)
)

data class LocationData(val lat: Double = 0.0, val lng: Double = 0.0)

class FirebaseRepository {
    private val db = FirebaseFirestore.getInstance()

    fun syncDeviceConfig(pairCode: String): Flow<DeviceConfig> = callbackFlow {
        val docRef = db.collection("devices").document(pairCode)
        val listener = docRef.addSnapshotListener { snapshot, error ->
            if (error != null) {
                return@addSnapshotListener
            }
            if (snapshot != null && snapshot.exists()) {
                val config = snapshot.toObject(DeviceConfig::class.java)
                if (config != null) {
                    trySend(config)
                }
            } else {
                // Initialize default config if it doesn't exist
                docRef.set(DeviceConfig())
                trySend(DeviceConfig())
            }
        }
        awaitClose { listener.remove() }
    }

    suspend fun updateConfig(pairCode: String, config: DeviceConfig) {
        db.collection("devices").document(pairCode).set(config).await()
    }
    
    suspend fun sendNotification(pairCode: String, notification: NotificationLog) {
        db.collection("devices").document(pairCode).collection("notifications").add(notification).await()
    }

    fun getNotifications(pairCode: String): Flow<List<NotificationLog>> = callbackFlow {
        val listener = db.collection("devices").document(pairCode).collection("notifications")
            .orderBy("timestamp")
            .addSnapshotListener { snapshot, error ->
                if (error != null) return@addSnapshotListener
                val logs = snapshot?.documents?.mapNotNull { it.toObject(NotificationLog::class.java) } ?: emptyList()
                trySend(logs)
            }
        awaitClose { listener.remove() }
    }
}
