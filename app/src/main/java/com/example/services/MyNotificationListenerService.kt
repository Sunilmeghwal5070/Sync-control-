package com.example.services

import android.app.Notification
import android.content.pm.PackageManager
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.util.Log
import com.example.data.AppDatabase
import com.example.data.FirebaseRepository
import com.example.data.NotificationLog
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

class MyNotificationListenerService : NotificationListenerService() {

    private val job = SupervisorJob()
    private val scope = CoroutineScope(Dispatchers.IO + job)
    private val firebaseRepository = FirebaseRepository()

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        super.onNotificationPosted(sbn)
        if (sbn == null) return
        
        val packageName = sbn.packageName
        val notification = sbn.notification
        val title = notification.extras.getCharSequence(Notification.EXTRA_TITLE)?.toString() ?: ""
        val text = notification.extras.getCharSequence(Notification.EXTRA_TEXT)?.toString() ?: ""
        
        if (title.isBlank() && text.isBlank()) return
        
        val content = if (title.isNotBlank()) "$title: $text" else text

        var appName = packageName
        try {
            val pm = applicationContext.packageManager
            val ai = pm.getApplicationInfo(packageName, 0)
            appName = pm.getApplicationLabel(ai).toString()
        } catch (e: Exception) {
            // fallback to package name
        }

        scope.launch {
            try {
                val db = AppDatabase.getDatabase(applicationContext)
                val devices = db.appDao().getPairedDevicesSync()
                val childDevice = devices.firstOrNull { it.role == "child" }
                if (childDevice != null && childDevice.isConnected) {
                    val configSnapshot = firebaseRepository.db.collection("devices").document(childDevice.pairCode).get().await()
                    if (configSnapshot.exists()) {
                        val config = configSnapshot.toObject(com.example.data.DeviceConfig::class.java)
                        if (config != null) {
                            val appInfo = config.installedApps.find { it.packageName == packageName }
                            if (appInfo != null && !appInfo.notificationsEnabled) {
                                return@launch
                            }
                        }
                    }
                    val log = NotificationLog(appName = appName, content = content, timestamp = System.currentTimeMillis())
                    firebaseRepository.sendNotification(childDevice.pairCode, log)
                }
            } catch (e: Exception) {
                Log.e("NotificationService", "Error sending notification", e)
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        job.cancel()
    }
}
