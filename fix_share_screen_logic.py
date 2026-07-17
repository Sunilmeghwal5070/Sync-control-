import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

replacement = """        if (role == "parent") {
            Spacer(modifier = Modifier.height(16.dp))
            Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Enter code of Child's Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = enteredCode,
                onValueChange = { if (it.length <= 10) enteredCode = it.uppercase() },
                placeholder = { Text("10-Digit Code", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)) },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = MaterialTheme.colorScheme.onBackground,
                    unfocusedTextColor = MaterialTheme.colorScheme.onBackground,
                )
            )
            Spacer(modifier = Modifier.height(24.dp))
        }

        val scope = androidx.compose.runtime.rememberCoroutineScope()
        var isVerifying by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
        var showPairingConfirmDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

        androidx.compose.runtime.LaunchedEffect(role, pairCode) {
            if (role == "child") {
                viewModel.initDeviceConfig(pairCode)
                viewModel.requestPairing(pairCode).collect { config ->
                    if (config?.pairingRequested == true && config.pairingAccepted == false) {
                        showPairingConfirmDialog = true
                    }
                }
            }
        }

        if (showPairingConfirmDialog) {
            AlertDialog(
                onDismissRequest = { },
                title = { Text("Pairing Request") },
                text = { Text("A parent device wants to connect to this device. Allow?") },
                confirmButton = {
                    Button(onClick = {
                        scope.launch {
                            viewModel.setPairingRequest(pairCode, requested = true, accepted = true)
                            viewModel.pairDevice(role, pairCode)
                            onPaired()
                            val apps = getInstalledApps(context)
                            viewModel.updateInstalledApps(apps)
                        }
                        showPairingConfirmDialog = false
                    }) {
                        Text("Accept")
                    }
                },
                dismissButton = {
                    Button(onClick = {
                        scope.launch {
                            viewModel.setPairingRequest(pairCode, requested = false, accepted = false)
                        }
                        showPairingConfirmDialog = false
                    }) {
                        Text("Reject")
                    }
                }
            )
        }

        if (role == "parent") {
            Button(
                onClick = {
                    val codeToUse = enteredCode
                    isVerifying = true
                    scope.launch {
                        val isValid = viewModel.verifyPairCode(codeToUse)
                        if (isValid) {
                            viewModel.setPairingRequest(codeToUse, requested = true, accepted = false)
                            viewModel.requestPairing(codeToUse).collect { config ->
                                if (config?.pairingAccepted == true) {
                                    viewModel.pairDevice(role, codeToUse)
                                    onPaired()
                                } else if (config?.pairingRequested == false) {
                                    isVerifying = false
                                    android.widget.Toast.makeText(context, "Pairing rejected by child", android.widget.Toast.LENGTH_LONG).show()
                                }
                            }
                        } else {
                            isVerifying = false
                            android.widget.Toast.makeText(context, "Invalid Code! Child must open app and show code first.", android.widget.Toast.LENGTH_LONG).show()
                        }
                    }
                },
                modifier = Modifier.width(200.dp).height(48.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                enabled = !isVerifying && enteredCode.length == 10
            ) {
                Text(if (isVerifying) "Waiting for approval..." else "Pair", color = MaterialTheme.colorScheme.onPrimary)
            }
        }"""

content = re.sub(r'        if \(role == "parent"\) \{\n            Spacer\(modifier = Modifier\.height\(16\.dp\)\)[\s\S]*?            Text\("Pair", color = MaterialTheme\.colorScheme\.onPrimary\)\n        \}', replacement, content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
