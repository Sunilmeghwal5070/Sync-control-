#!/bin/bash
sed -i '/fun AppHiderScreen(deviceConfig:/,/^    }*$/c\
@OptIn(ExperimentalMaterial3Api::class)\
@Composable\
fun AppHiderScreen(deviceConfig: DeviceConfig, onConfigChanged: (DeviceConfig) -> Unit, onBack: () -> Unit) {\
    var showAppLockDialog by remember { mutableStateOf(false) }\
    var showAppHideDialog by remember { mutableStateOf(false) }\
    Scaffold(\
        topBar = {\
            TopAppBar(\
                title = { Text("App Hider & Restrictions") },\
                navigationIcon = {\
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }\
                }\
            )\
        }\
    ) { padding ->\
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {\
            item {\
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {\
                    Column(modifier = Modifier.padding(16.dp)) {\
                        Text("App Hider & Lock", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)\
                        Text("Select apps to hide or lock on child'\''s device.", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f), fontSize = 14.sp)\
                        Spacer(modifier = Modifier.height(16.dp))\
                        Button(onClick = { showAppLockDialog = true }, modifier = Modifier.fillMaxWidth()) { Text("Manage App Locks") }\
                        Spacer(modifier = Modifier.height(8.dp))\
                        Button(onClick = { showAppHideDialog = true }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) { Text("Manage Hidden Apps", color = MaterialTheme.colorScheme.onSurface) }\
                    }\
                }\
                Spacer(modifier = Modifier.height(16.dp))\
            }\
            item {\
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {\
                    Column(modifier = Modifier.padding(16.dp)) {\
                        Text("Web Filtering & Blocking", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)\
                        Text("Block websites and domains.", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f), fontSize = 14.sp)\
                        Spacer(modifier = Modifier.height(16.dp))\
                        Button(onClick = {}, modifier = Modifier.fillMaxWidth()) { Text("Manage Blocked Websites") }\
                    }\
                }\
                Spacer(modifier = Modifier.height(16.dp))\
            }\
        }\
        \
        if (showAppLockDialog) {\
            AppSelectionDialog(\
                title = "Lock Apps",\
                apps = deviceConfig.installedApps,\
                isHiding = false,\
                onToggle = { app, isLocked ->\
                    val newApps = deviceConfig.installedApps.map {\
                        if (it.packageName == app.packageName) it.copy(isLocked = isLocked) else it\
                    }\
                    onConfigChanged(deviceConfig.copy(installedApps = newApps))\
                },\
                onDismiss = { showAppLockDialog = false }\
            )\
        }\
        if (showAppHideDialog) {\
            AppSelectionDialog(\
                title = "Hide Apps",\
                apps = deviceConfig.installedApps,\
                isHiding = true,\
                onToggle = { app, isHidden ->\
                    val newApps = deviceConfig.installedApps.map {\
                        if (it.packageName == app.packageName) it.copy(isHidden = isHidden) else it\
                    }\
                    onConfigChanged(deviceConfig.copy(installedApps = newApps))\
                },\
                onDismiss = { showAppHideDialog = false }\
            )\
        }\
    }\
}\
' app/src/main/java/com/example/ui/screens/ParentScreens.kt
