import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """    if (!acceptedTerms) {
        androidx.activity.compose.BackHandler { onBack() }
        AlertDialog(
            onDismissRequest = onBack,
            title = { Text("Read Carefully", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth(), fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("1. This app uses third party(Firebase) services to share Notifications. End-to-end encryption ensures only you can read and nobody in between.")
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("2. You are responsible for your Child notifications.")
                }
            },
            confirmButton = {
                Button(
                    onClick = { acceptedTerms = true },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Accept", color = MaterialTheme.colorScheme.onPrimary)
                }
            },
            dismissButton = {
                TextButton(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
                    Text("Decline", color = MaterialTheme.colorScheme.onSurface)
                }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    } else {
        // Allow back when terms are accepted
        androidx.activity.compose.BackHandler { onBack() }
    }"""
replacement = """    // Removed blocking dialog to prevent trapping user.
    // Let system handle back button naturally.
    """
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
