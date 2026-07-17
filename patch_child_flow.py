import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """                val childJob = scope.launch {
                    viewModel.requestPairing(pairCode).collect { config ->
                        if (config?.pairingRequested == true && config.pairingAccepted == false) {
                            showPairingConfirmDialog = true
                        }
                    }
                }"""
replacement = """                kotlinx.coroutines.launch {
                    viewModel.requestPairing(pairCode).collect { config ->
                        if (config?.pairingRequested == true && config.pairingAccepted == false) {
                            showPairingConfirmDialog = true
                        }
                    }
                }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
