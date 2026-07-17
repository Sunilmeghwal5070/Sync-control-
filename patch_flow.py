import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """                            viewModel.requestPairing(codeToUse).collect { config ->
                                if (config?.pairingAccepted == true) {
                                    viewModel.pairDevice(role, codeToUse)
                                    onPaired()
                                } else if (config?.pairingRequested == false) {
                                    isVerifying = false
                                    android.widget.Toast.makeText(context, "Pairing rejected by child", android.widget.Toast.LENGTH_LONG).show()
                                }
                            }"""
replacement = """                            val job = scope.launch {
                                viewModel.requestPairing(codeToUse).collect { config ->
                                    if (config?.pairingAccepted == true) {
                                        viewModel.pairDevice(role, codeToUse)
                                        onPaired()
                                        this@launch.cancel()
                                    } else if (config?.pairingRequested == false) {
                                        isVerifying = false
                                        android.widget.Toast.makeText(context, "Pairing rejected by child", android.widget.Toast.LENGTH_LONG).show()
                                        this@launch.cancel()
                                    }
                                }
                            }"""
content = content.replace(target, replacement)

target_child = """                viewModel.requestPairing(pairCode).collect { config ->
                    if (config?.pairingRequested == true && config.pairingAccepted == false) {
                        showPairingConfirmDialog = true
                    }
                }"""
replacement_child = """                val childJob = scope.launch {
                    viewModel.requestPairing(pairCode).collect { config ->
                        if (config?.pairingRequested == true && config.pairingAccepted == false) {
                            showPairingConfirmDialog = true
                        }
                    }
                }"""
content = content.replace(target_child, replacement_child)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
