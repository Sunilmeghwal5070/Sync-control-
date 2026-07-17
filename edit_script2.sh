#!/bin/bash
sed -i '/fun PermissionScreen(role:/,/fun PermissionItem/c\
@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\
@Composable\
fun PermissionScreen(role: String, onPermissionsGranted: () -> Unit) {\
    if (role == "parent") {\
        Column(\
            modifier = Modifier\
                .fillMaxSize()\
                .background(MaterialTheme.colorScheme.background)\
                .padding(24.dp),\
            horizontalAlignment = Alignment.CenterHorizontally,\
            verticalArrangement = Arrangement.Center\
        ) {\
            Text("Parent Setup", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)\
            Spacer(modifier = Modifier.height(32.dp))\
            Button(onClick = onPermissionsGranted, modifier = Modifier.fillMaxWidth().height(50.dp)) {\
                Text("Continue to Pairing")\
            }\
        }\
        return\
    }\
\
    val context = androidx.compose.ui.platform.LocalContext.current\
    var notifGranted by remember { mutableStateOf(false) }\
    var adminGranted by remember { mutableStateOf(false) }\
    var accessGranted by remember { mutableStateOf(false) }\
    var overlayGranted by remember { mutableStateOf(false) }\
\
    val locationPermissionState = com.google.accompanist.permissions.rememberMultiplePermissionsState(\
        permissions = listOf(\
            android.Manifest.permission.ACCESS_FINE_LOCATION,\
            android.Manifest.permission.ACCESS_COARSE_LOCATION\
        )\
    )\
    val cameraPermissionState = com.google.accompanist.permissions.rememberMultiplePermissionsState(\
        permissions = listOf(\
            android.Manifest.permission.CAMERA,\
            android.Manifest.permission.RECORD_AUDIO\
        )\
    )\
\
    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState.allPermissionsGranted && cameraPermissionState.allPermissionsGranted && overlayGranted\
    var showWarning by remember { mutableStateOf(false) }\
\
    Column(\
        modifier = Modifier\
            .fillMaxSize()\
            .background(MaterialTheme.colorScheme.background)\
            .padding(16.dp),\
        horizontalAlignment = Alignment.CenterHorizontally\
    ) {\
        Text(\
            text = "Required Permissions",\
            fontSize = 24.sp,\
            fontWeight = FontWeight.Bold,\
            color = MaterialTheme.colorScheme.primary,\
            modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)\
        )\
        Text(\
            text = "Please allow all permissions for full functionality and security.",\
            fontSize = 14.sp,\
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f),\
            textAlign = TextAlign.Center,\
            modifier = Modifier.padding(bottom = 16.dp)\
        )\
\
        LazyColumn(\
            modifier = Modifier.weight(1f),\
            verticalArrangement = Arrangement.spacedBy(8.dp)\
        ) {\
            item {\
                PermissionItem(\
                    title = "Notification Access",\
                    description = "Required to sync notifications to parent.",\
                    isGranted = notifGranted,\
                    onGrant = { \
                        val intent = android.content.Intent(android.provider.Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)\
                        context.startActivity(intent)\
                        notifGranted = true \
                    }\
                )\
            }\
            item {\
                PermissionItem(\
                    title = "Device Administrator",\
                    description = "Required to lock/wipe device remotely.",\
                    isGranted = adminGranted,\
                    onGrant = { \
                        val intent = android.content.Intent(android.provider.Settings.ACTION_SECURITY_SETTINGS)\
                        context.startActivity(intent)\
                        adminGranted = true \
                    }\
                )\
            }\
            item {\
                PermissionItem(\
                    title = "Accessibility Service",\
                    description = "Required for app limits and web filtering.",\
                    isGranted = accessGranted,\
                    onGrant = { \
                        val intent = android.content.Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)\
                        context.startActivity(intent)\
                        accessGranted = true \
                    }\
                )\
            }\
            item {\
                PermissionItem(\
                    title = "Location Access",\
                    description = "Required for real-time location tracking.",\
                    isGranted = locationPermissionState.allPermissionsGranted,\
                    onGrant = { locationPermissionState.launchMultiplePermissionRequest() }\
                )\
            }\
            item {\
                PermissionItem(\
                    title = "Camera & Microphone",\
                    description = "Required for remote camera and ambient audio.",\
                    isGranted = cameraPermissionState.allPermissionsGranted,\
                    onGrant = { cameraPermissionState.launchMultiplePermissionRequest() }\
                )\
            }\
            item {\
                PermissionItem(\
                    title = "Display over other apps",\
                    description = "Required for app lock screen overlays.",\
                    isGranted = overlayGranted,\
                    onGrant = { \
                        val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION)\
                        context.startActivity(intent)\
                        overlayGranted = true \
                    }\
                )\
            }\
        }\
\
        if (showWarning) {\
            Text(\
                "You must allow ALL permissions to continue.",\
                color = Color.Red,\
                fontWeight = FontWeight.Bold,\
                modifier = Modifier.padding(vertical = 8.dp)\
            )\
        }\
\
        Button(\
            onClick = {\
                if (allGranted) {\
                    onPermissionsGranted()\
                } else {\
                    showWarning = true\
                }\
            },\
            modifier = Modifier\
                .fillMaxWidth()\
                .padding(bottom = 16.dp)\
                .height(50.dp),\
            colors = ButtonDefaults.buttonColors(\
                containerColor = if (allGranted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,\
                contentColor = if (allGranted) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface\
            )\
        ) {\
            Text("Continue")\
        }\
    }\
}\
\
@Composable\
fun PermissionItem' app/src/main/java/com/example/ui/screens/MainScreens.kt
