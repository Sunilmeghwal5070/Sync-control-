#!/bin/bash
sed -i '/val pairCode = remember { viewModel.generatePairCode() }/a\
    val scope = androidx.compose.runtime.rememberCoroutineScope()\
    var isVerifying by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }' app/src/main/java/com/example/ui/screens/MainScreens.kt

sed -i '/onClick = {/,/            enabled = role == "child" || enteredCode.length == 6/c\
            onClick = {\
                val codeToUse = if (role == "child") pairCode else enteredCode\
                if (role == "parent") {\
                    isVerifying = true\
                    scope.kotlinx.coroutines.launch {\
                        val isValid = viewModel.verifyPairCode(codeToUse)\
                        isVerifying = false\
                        if (isValid) {\
                            viewModel.pairDevice(role, codeToUse)\
                            onPaired()\
                        } else {\
                            android.widget.Toast.makeText(context, "Invalid Pair Code. Child must open the app first.", android.widget.Toast.LENGTH_LONG).show()\
                        }\
                    }\
                } else {\
                    scope.kotlinx.coroutines.launch {\
                        viewModel.initDeviceConfig(codeToUse)\
                        viewModel.pairDevice(role, codeToUse)\
                        onPaired()\
                        val apps = getInstalledApps(context)\
                        viewModel.updateInstalledApps(apps)\
                    }\
                }\
            },\
            modifier = Modifier.width(120.dp).height(48.dp),\
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),\
            enabled = !isVerifying && (role == "child" || enteredCode.length == 6)' app/src/main/java/com/example/ui/screens/MainScreens.kt
