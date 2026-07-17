package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "paired_devices")
data class PairedDevice(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val role: String, // "parent" or "child"
    val pairCode: String,
    val isConnected: Boolean = false,
    val deviceName: String = "Child Device"
)

@Entity(tableName = "notification_logs")
data class NotificationLog(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val appName: String = "",
    val content: String = "",
    val timestamp: Long = System.currentTimeMillis()
)
