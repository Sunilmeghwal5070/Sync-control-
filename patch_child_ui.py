with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """        Text("Simulate Activity", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)"""

replacement = """        var showNotificationSettings by remember { mutableStateOf(false) }
        Button(
            onClick = { showNotificationSettings = true },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
        ) {
            Text("Notification Settings", fontSize = 16.sp)
        }
        
        if (showNotificationSettings) {
            AlertDialog(
                onDismissRequest = { showNotificationSettings = false },
                title = { Text("App Notification Settings") },
                text = {
                    LazyColumn {
                        items(deviceConfig.installedApps) { app ->
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(app.appName, modifier = Modifier.weight(1f))
                                Switch(
                                    checked = app.notificationsEnabled,
                                    onCheckedChange = { isEnabled ->
                                        val updatedList = deviceConfig.installedApps.map {
                                            if (it.packageName == app.packageName) it.copy(notificationsEnabled = isEnabled) else it
                                        }
                                        onUpdateAppStatus(updatedList)
                                    }
                                )
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showNotificationSettings = false }) {
                        Text("Close")
                    }
                }
            )
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        Text("Simulate Activity", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)"""

content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
