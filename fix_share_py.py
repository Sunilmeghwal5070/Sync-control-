import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

# Replace OR ... OutlinedTextField ... Button
replacement = """        if (role == "parent") {
            Spacer(modifier = Modifier.height(16.dp))
            Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Enter code of Child's Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = enteredCode,
                onValueChange = { if (it.length <= 6) enteredCode = it.uppercase() },
                placeholder = { Text("6-Digit Code", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)) },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = MaterialTheme.colorScheme.onBackground,
                    unfocusedTextColor = MaterialTheme.colorScheme.onBackground,
                )
            )
        }
        Spacer(modifier = Modifier.height(24.dp))
        val scope = androidx.compose.runtime.rememberCoroutineScope()
        var isVerifying by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
        
        Button(
            onClick = {
                val codeToUse = if (role == "child") pairCode else enteredCode
                if (role == "parent") {
                    isVerifying = true
                    scope.launch {
                        val isValid = viewModel.verifyPairCode(codeToUse)
                        isVerifying = false
                        if (isValid) {
                            viewModel.pairDevice(role, codeToUse)
                            onPaired()
                        } else {
                            android.widget.Toast.makeText(context, "Invalid Code! Child must open app and show code first.", android.widget.Toast.LENGTH_LONG).show()
                        }
                    }
                } else {
                    scope.launch {
                        viewModel.initDeviceConfig(codeToUse)
                        viewModel.pairDevice(role, codeToUse)
                        onPaired()
                        val apps = getInstalledApps(context)
                        viewModel.updateInstalledApps(apps)
                    }
                }
            },
            modifier = Modifier.width(120.dp).height(48.dp),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
            enabled = !isVerifying && (role == "child" || enteredCode.length == 6)
        ) {"""

content = re.sub(r'        Spacer\(modifier = Modifier\.height\(16\.dp\)\)\n        Text\("OR"[\s\S]*?        Button\([\s\S]*?        \) \{', replacement, content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
