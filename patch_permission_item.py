import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """    var overlayGranted by remember { mutableStateOf(android.provider.Settings.canDrawOverlays(context)) }"""
replacement = """    var overlayGranted by remember { mutableStateOf(android.provider.Settings.canDrawOverlays(context)) }
    var writeSettingsGranted by remember { mutableStateOf(android.provider.Settings.System.canWrite(context)) }"""
content = content.replace(target, replacement)

target2 = """            overlayGranted = android.provider.Settings.canDrawOverlays(context)"""
replacement2 = """            overlayGranted = android.provider.Settings.canDrawOverlays(context)
            writeSettingsGranted = android.provider.Settings.System.canWrite(context)"""
content = content.replace(target2, replacement2)

target3 = """    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState.allPermissionsGranted && cameraPermissionState.allPermissionsGranted && overlayGranted"""
replacement3 = """    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState.allPermissionsGranted && cameraPermissionState.allPermissionsGranted && overlayGranted && writeSettingsGranted"""
content = content.replace(target3, replacement3)

target4 = """            item {
                PermissionItem(
                    title = "Display over other apps",
                    description = "Required for app lock screen overlays.",
                    isGranted = overlayGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:" + context.packageName))
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); overlayGranted = true }
                    }
                )
            }"""
replacement4 = """            item {
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
            item {
                PermissionItem(
                    title = "Modify System Settings",
                    description = "Required to control WiFi, brightness, etc.",
                    isGranted = writeSettingsGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_WRITE_SETTINGS, android.net.Uri.parse("package:" + context.packageName))
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); writeSettingsGranted = true }
                    }
                )
            }"""
content = content.replace(target4, replacement4)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
