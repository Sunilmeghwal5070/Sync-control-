#!/bin/bash
sed -i '/fun pairDevice(role: String, code: String)/i\
    fun disconnectDevice(pairCode: String? = null) {\
        viewModelScope.launch {\
            val codeToDisconnect = pairCode ?: _selectedPairCode.value\
            if (codeToDisconnect != null) {\
                val device = allPairedDevices.value.find { it.pairCode == codeToDisconnect }\
                if (device != null) {\
                    repository.savePairedDevice(device.copy(isConnected = false))\
                }\
                if (pairCode == null || pairCode == _selectedPairCode.value) {\
                    _selectedPairCode.value = null\
                }\
            }\
        }\
    }\
' app/src/main/java/com/example/viewmodel/AppViewModel.kt
