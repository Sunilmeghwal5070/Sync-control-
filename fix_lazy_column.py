import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

replacement = """        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            item {
                PermissionItem(
                    title = "Notification Access",
                    description = "Required to sync notifications to parent.",
                    isGranted = notifGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); notifGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Device Administrator",
                    description = "Required to lock/wipe device remotely.",
                    isGranted = adminGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.app.admin.DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN).apply { putExtra(android.app.admin.DevicePolicyManager.EXTRA_DEVICE_ADMIN, android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java)) }
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); adminGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Accessibility Service",
                    description = "Required for app limits and web filtering.",
                    isGranted = accessGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); accessGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Location Access",
                    description = "Required for real-time location tracking.",
                    isGranted = locationPermissionState.allPermissionsGranted,
                    onGrant = { locationPermissionState.launchMultiplePermissionRequest() }
                )
            }
            item {
                PermissionItem(
                    title = "Camera & Microphone",
                    description = "Required for remote camera and ambient audio.",
                    isGranted = cameraPermissionState.allPermissionsGranted,
                    onGrant = { cameraPermissionState.launchMultiplePermissionRequest() }
                )
            }
            item {
                PermissionItem(
                    title = "Display over other apps",
                    description = "Required for app lock screen overlays.",
                    isGranted = overlayGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:" + context.packageName))
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); overlayGranted = true }
                    }
                )
            }
        }"""

content = re.sub(r'        LazyColumn\([\s\S]*?        }\n\n        if \(showWarning\) {', replacement + '\n\n        if (showWarning) {', content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
