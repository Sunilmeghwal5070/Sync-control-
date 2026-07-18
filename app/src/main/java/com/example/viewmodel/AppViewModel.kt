package com.example.viewmodel

import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.tasks.await

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.AppInfo
import com.example.data.AppRepository
import com.example.data.DeviceConfig
import com.example.data.FirebaseRepository
import com.example.data.NotificationLog
import com.example.data.PairedDevice
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class AppViewModel(
    private val repository: AppRepository,
    private val firebaseRepository: FirebaseRepository
) : ViewModel() {

    val allPairedDevices: StateFlow<List<PairedDevice>> = repository.allPairedDevices
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val pairedDevice: StateFlow<PairedDevice?> = repository.pairedDevice
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
        
    private val _selectedPairCode = MutableStateFlow<String?>(null)
    val selectedPairCode: StateFlow<String?> = _selectedPairCode.asStateFlow()

    private val _notificationLogs = MutableStateFlow<List<NotificationLog>>(emptyList())
    val notificationLogs: StateFlow<List<NotificationLog>> = _notificationLogs.asStateFlow()
    
    private val _deviceConfig = MutableStateFlow(DeviceConfig())
    val deviceConfig: StateFlow<DeviceConfig> = _deviceConfig.asStateFlow()

    init {
        viewModelScope.launch {
            _selectedPairCode.collectLatest { pairCode ->
                if (pairCode != null) {
                    launch {
                        firebaseRepository.syncDeviceConfig(pairCode).collect { config ->
                            _deviceConfig.value = config
                        }
                    }
                    launch {
                        firebaseRepository.getNotifications(pairCode).collect { logs ->
                            _notificationLogs.value = logs
                        }
                    }
                } else {
                    _notificationLogs.value = emptyList()
                    _deviceConfig.value = DeviceConfig()
                }
            }
        }
        
        viewModelScope.launch {
            allPairedDevices.collectLatest { devices ->
                val childDevice = devices.firstOrNull { it.role == "child" }
                if (childDevice != null) {
                    _selectedPairCode.value = childDevice.pairCode
                } else if (devices.isNotEmpty() && _selectedPairCode.value == null) {
                    _selectedPairCode.value = devices.first().pairCode
                }
            }
        }
    }

    fun selectDevice(pairCode: String) {
        _selectedPairCode.value = pairCode
    }

    fun disconnectDevice(pairCode: String? = null) {
        viewModelScope.launch {
            val codeToDisconnect = pairCode ?: _selectedPairCode.value
            if (codeToDisconnect != null) {
                val device = allPairedDevices.value.find { it.pairCode == codeToDisconnect }
                if (device != null) {
                    repository.savePairedDevice(device.copy(isConnected = false))
                }
                if (pairCode == null || pairCode == _selectedPairCode.value) {
                    _selectedPairCode.value = null
                }
            }
        }
    }

    suspend fun requestPairing(code: String): kotlinx.coroutines.flow.Flow<DeviceConfig?> {
        return firebaseRepository.syncDeviceConfig(code)
    }

    suspend fun setPairingRequest(code: String, requested: Boolean, accepted: Boolean) {
        val currentConfig = firebaseRepository.syncDeviceConfig(code).first()
        
        // Auto-accept if requested but not accepted (Mock auto-pair for single-device emulator)
        val finalAccepted = if (requested && !accepted) true else accepted
        
        firebaseRepository.updateConfig(code, currentConfig.copy(pairingRequested = requested, pairingAccepted = finalAccepted))
    }

    suspend fun verifyPairCode(code: String): Pair<Boolean, String?> {
        return firebaseRepository.verifyConfigExists(code)
    }

    suspend fun initDeviceConfig(code: String): String? {
        return try {
            firebaseRepository.updateConfig(code, DeviceConfig())
            null
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "initDeviceConfig error", e)
            e.message
        }
    }

    fun pairDevice(role: String, code: String) {
        viewModelScope.launch {
            val deviceName = if (role == "parent") "Child Device ${allPairedDevices.value.size + 1}" else "Child Device"
            repository.savePairedDevice(PairedDevice(role = role, pairCode = code, isConnected = true, deviceName = deviceName))
            _selectedPairCode.value = code
        }
    }
    
    fun updateConfig(newConfig: DeviceConfig) {
        val currentPairCode = _selectedPairCode.value
        if (currentPairCode != null) {
            viewModelScope.launch {
                firebaseRepository.updateConfig(currentPairCode, newConfig)
            }
        }
    }
    
    fun updateInstalledApps(apps: List<AppInfo>) {
        val currentPairCode = _selectedPairCode.value
        if (currentPairCode != null) {
            viewModelScope.launch {
                val currentApps = _deviceConfig.value.installedApps
                val mergedApps = apps.map { newApp ->
                    val existing = currentApps.find { it.packageName == newApp.packageName }
                    if (existing != null) {
                        newApp.copy(isLocked = existing.isLocked, isHidden = existing.isHidden, notificationsEnabled = existing.notificationsEnabled)
                    } else {
                        newApp
                    }
                }
                val newConfig = _deviceConfig.value.copy(installedApps = mergedApps)
                firebaseRepository.updateConfig(currentPairCode, newConfig)
            }
        }
    }
    
    // For Child to send notifications
    fun sendNotification(appName: String, content: String) {
        val currentDevice = allPairedDevices.value.firstOrNull { it.role == "child" }
        if (currentDevice != null && currentDevice.isConnected) {
            val appInfo = _deviceConfig.value.installedApps.find { it.appName.equals(appName, ignoreCase = true) || it.packageName == appName }
            if (appInfo != null && !appInfo.notificationsEnabled) {
                // Notifications for this app are disabled by the parent/child
                return
            }
            viewModelScope.launch {
                val log = NotificationLog(appName = appName, content = content, timestamp = System.currentTimeMillis())
                firebaseRepository.sendNotification(currentDevice.pairCode, log)
            }
        }
    }
    
    private var currentPairCode: String? = null
    private var pairCodeGenerationTime: Long = 0

    fun generatePairCode(): String {
        if (currentPairCode == null) {
            val chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            currentPairCode = (1..10).map { chars.random() }.joinToString("")
        }
        return currentPairCode!!
    }
    
    fun refreshPairCode(): String {
        val chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        currentPairCode = (1..10).map { chars.random() }.joinToString("")
        return currentPairCode!!
    }
}

class AppViewModelFactory(
    private val repository: AppRepository,
    private val firebaseRepository: FirebaseRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(AppViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return AppViewModel(repository, firebaseRepository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
