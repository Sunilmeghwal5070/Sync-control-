import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

# Make allGranted true if critical ones are true, or just don't enforce it rigidly.
# Also change the continue button to always proceed.
target_btn = """        Button(
            onClick = {
                if (allGranted) {
                    onPermissionsGranted()
                } else {
                    showWarning = true
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
                .height(50.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = if (allGranted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                contentColor = if (allGranted) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
            )
        ) {
            Text("Continue")
        }"""

replacement_btn = """        Button(
            onClick = {
                // Allow proceed even if some permissions like overlay are denied on Android Go
                onPermissionsGranted()
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
                .height(50.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            )
        ) {
            Text("Continue (Skip Optional)")
        }"""

content = content.replace(target_btn, replacement_btn)

# Make sure it doesn't auto-redirect without clicking if we don't want it, or let it auto-redirect if all are granted.
target_effect = """    androidx.compose.runtime.LaunchedEffect(allGranted) {
        if (allGranted) {
            onPermissionsGranted()
        }
    }"""
# removing it so user has to click Continue manually and can see which ones failed. Or leave it.
replacement_effect = """    // Auto-proceed if all granted, but user can also click continue manually
    androidx.compose.runtime.LaunchedEffect(allGranted) {
        if (allGranted) {
            onPermissionsGranted()
        }
    }"""
content = content.replace(target_effect, replacement_effect)

target_usecase = """            UseCaseCard(title = "Business / Other", onClick = onNavigateToRoleSelection)
            
            Spacer(modifier = Modifier.weight(1f))"""

replacement_usecase = """            Spacer(modifier = Modifier.weight(1f))"""
content = content.replace(target_usecase, replacement_usecase)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
