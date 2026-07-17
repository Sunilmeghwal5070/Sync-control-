import re

# FirebaseRepository.kt
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    fr_content = f.read()

fr_target = """    suspend fun verifyConfigExists(pairCode: String): Boolean {
        val snapshot = db.collection("devices").document(pairCode).get().await()
        return snapshot.exists()
    }"""
fr_replacement = """    suspend fun verifyConfigExists(pairCode: String): Pair<Boolean, String?> {
        return try {
            val snapshot = db.collection("devices").document(pairCode).get().await()
            Pair(snapshot.exists(), null)
        } catch (e: Exception) {
            Pair(false, e.message)
        }
    }"""
fr_content = fr_content.replace(fr_target, fr_replacement)
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(fr_content)

# AppViewModel.kt
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    av_content = f.read()

av_target1 = """    suspend fun verifyPairCode(code: String): Boolean {
        return try {
            val snapshot = firebaseRepository.verifyConfigExists(code)
            snapshot
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "verifyPairCode error", e)
            false
        }
    }"""
av_replacement1 = """    suspend fun verifyPairCode(code: String): Pair<Boolean, String?> {
        return firebaseRepository.verifyConfigExists(code)
    }"""
av_content = av_content.replace(av_target1, av_replacement1)

av_target2 = """    suspend fun initDeviceConfig(code: String) {
        try {
            firebaseRepository.updateConfig(code, DeviceConfig())
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "initDeviceConfig error", e)
        }
    }"""
av_replacement2 = """    suspend fun initDeviceConfig(code: String): String? {
        return try {
            firebaseRepository.updateConfig(code, DeviceConfig())
            null
        } catch (e: Exception) {
            android.util.Log.e("AppViewModel", "initDeviceConfig error", e)
            e.message
        }
    }"""
av_content = av_content.replace(av_target2, av_replacement2)
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(av_content)

# MainScreens.kt
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    ms_content = f.read()

ms_target1 = """                viewModel.initDeviceConfig(pairCode)
                viewModel.requestPairing(pairCode).collect { config ->"""
ms_replacement1 = """                val initErr = viewModel.initDeviceConfig(pairCode)
                if (initErr != null) {
                    android.widget.Toast.makeText(context, "Firebase DB Error on Child: $initErr", android.widget.Toast.LENGTH_LONG).show()
                }
                viewModel.requestPairing(pairCode).collect { config ->"""
ms_content = ms_content.replace(ms_target1, ms_replacement1)

ms_target2 = """                        val isValid = viewModel.verifyPairCode(codeToUse)
                        if (isValid) {"""
ms_replacement2 = """                        val (isValid, errorMsg) = viewModel.verifyPairCode(codeToUse)
                        if (isValid) {"""
ms_content = ms_content.replace(ms_target2, ms_replacement2)

ms_target3 = """                        } else {
                            isVerifying = false
                            android.widget.Toast.makeText(context, "Invalid Code! Child must open app and show code first.", android.widget.Toast.LENGTH_LONG).show()
                        }"""
ms_replacement3 = """                        } else {
                            isVerifying = false
                            if (errorMsg != null) {
                                android.widget.Toast.makeText(context, "Firebase Error: $errorMsg", android.widget.Toast.LENGTH_LONG).show()
                            } else {
                                android.widget.Toast.makeText(context, "Invalid Code! Child must open app and show code first.", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }"""
ms_content = ms_content.replace(ms_target3, ms_replacement3)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(ms_content)

