import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """                kotlinx.coroutines.launch {
                    viewModel.requestPairing(pairCode).collect { config ->"""
replacement = """                launch {
                    viewModel.requestPairing(pairCode).collect { config ->"""
content = content.replace(target, replacement)

target2 = """                            val job = scope.launch {
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
replacement2 = """                            scope.launch {
                                viewModel.requestPairing(codeToUse).collect { config ->
                                    if (config?.pairingAccepted == true) {
                                        viewModel.pairDevice(role, codeToUse)
                                        onPaired()
                                    } else if (config?.pairingRequested == false) {
                                        isVerifying = false
                                        // Wait until user triggers again
                                    }
                                }
                            }"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
