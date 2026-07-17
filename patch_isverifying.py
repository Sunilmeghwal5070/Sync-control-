import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """                        if (isValid) {
                            viewModel.setPairingRequest(codeToUse, requested = true, accepted = false)
                            scope.launch {
                                viewModel.requestPairing(codeToUse).collect { config ->"""
replacement = """                        if (isValid) {
                            try {
                                viewModel.setPairingRequest(codeToUse, requested = true, accepted = false)
                            } catch (e: Exception) {
                                isVerifying = false
                                android.widget.Toast.makeText(context, "Pairing request failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
                                return@launch
                            }
                            scope.launch {
                                viewModel.requestPairing(codeToUse).collect { config ->"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
