package com.example.data

import kotlinx.coroutines.flow.Flow

class AppRepository(private val appDao: AppDao) {
    val pairedDevice: Flow<PairedDevice?> = appDao.getPairedDevice()
    val allPairedDevices: Flow<List<PairedDevice>> = appDao.getAllPairedDevices()
    
    val notificationLogs: Flow<List<NotificationLog>> = appDao.getNotificationLogs()

    suspend fun savePairedDevice(device: PairedDevice) {
        appDao.savePairedDevice(device)
    }

    suspend fun clearPairedDevice() {
        appDao.clearPairedDevice()
    }
    
    suspend fun deletePairedDevice(pairCode: String) {
        appDao.deletePairedDevice(pairCode)
    }

    suspend fun insertNotificationLog(log: NotificationLog) {
        appDao.insertNotificationLog(log)
    }
    
    suspend fun clearNotificationLogs() {
        appDao.clearNotificationLogs()
    }
}
