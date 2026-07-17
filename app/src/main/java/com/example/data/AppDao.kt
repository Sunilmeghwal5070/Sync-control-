package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface AppDao {
    @Query("SELECT * FROM paired_devices LIMIT 1")
    fun getPairedDevice(): Flow<PairedDevice?>

    @Query("SELECT * FROM paired_devices")
    fun getAllPairedDevices(): Flow<List<PairedDevice>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun savePairedDevice(device: PairedDevice)

    @Query("DELETE FROM paired_devices")
    suspend fun clearPairedDevice()
    
    @Query("DELETE FROM paired_devices WHERE pairCode = :pairCode")
    suspend fun deletePairedDevice(pairCode: String)

    @Query("SELECT * FROM notification_logs ORDER BY timestamp DESC")
    fun getNotificationLogs(): Flow<List<NotificationLog>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertNotificationLog(log: NotificationLog)
    
    @Query("DELETE FROM notification_logs")
    suspend fun clearNotificationLogs()
}
