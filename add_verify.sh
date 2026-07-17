#!/bin/bash
sed -i '/fun pairDevice(role: String, code: String)/i\
    suspend fun verifyPairCode(code: String): Boolean {\
        return try {\
            val snapshot = firebaseRepository.verifyConfigExists(code)\
            snapshot\
        } catch (e: Exception) {\
            false\
        }\
    }\
\
    suspend fun initDeviceConfig(code: String) {\
        firebaseRepository.updateConfig(code, DeviceConfig())\
    }\
' app/src/main/java/com/example/viewmodel/AppViewModel.kt
