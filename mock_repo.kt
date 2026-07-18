package com.example.data

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.delay

object MockDatabase {
    val devices = mutableMapOf<String, MutableStateFlow<DeviceConfig>>()
    val notifications = mutableMapOf<String, MutableStateFlow<List<NotificationLog>>>()

    fun getDeviceFlow(pairCode: String): MutableStateFlow<DeviceConfig> {
        return devices.getOrPut(pairCode) { MutableStateFlow(DeviceConfig()) }
    }
    
    fun getNotificationsFlow(pairCode: String): MutableStateFlow<List<NotificationLog>> {
        return notifications.getOrPut(pairCode) { MutableStateFlow(emptyList()) }
    }
}

class FirebaseRepository {
    fun syncDeviceConfig(pairCode: String): Flow<DeviceConfig> {
        return MockDatabase.getDeviceFlow(pairCode)
    }

    suspend fun verifyConfigExists(pairCode: String): Pair<Boolean, String?> {
        delay(500) // Simulate network
        val exists = MockDatabase.devices.containsKey(pairCode)
        return if (exists) Pair(true, null) else Pair(false, "Invalid Pair Code or Child disconnected")
    }

    suspend fun updateConfig(pairCode: String, config: DeviceConfig) {
        MockDatabase.getDeviceFlow(pairCode).value = config
    }
    
    suspend fun sendNotification(pairCode: String, notification: NotificationLog) {
        val flow = MockDatabase.getNotificationsFlow(pairCode)
        flow.value = flow.value + notification
    }

    fun getNotifications(pairCode: String): Flow<List<NotificationLog>> {
        return MockDatabase.getNotificationsFlow(pairCode)
    }
}
