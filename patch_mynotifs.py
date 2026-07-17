import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyNotificationsScreen(viewModel: AppViewModel, onBack: () -> Unit) {"""
replacement = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyNotificationsScreen(viewModel: AppViewModel, onBack: () -> Unit) {
    val deviceConfig by viewModel.deviceConfig.collectAsStateWithLifecycle()
    var showNotificationSettings by remember { mutableStateOf(false) }
"""
content = content.replace(target, replacement)

target2 = """                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onSurface)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { padding ->"""
replacement2 = """                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onSurface)
                    }
                },
                actions = {
                    IconButton(onClick = { showNotificationSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "App Settings", tint = MaterialTheme.colorScheme.onSurface)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { padding ->
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
                                        viewModel.updateInstalledApps(updatedList)
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
        }"""
content = content.replace(target2, replacement2)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
