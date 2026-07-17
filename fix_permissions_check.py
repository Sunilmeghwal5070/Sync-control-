import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

replacement = """    val context = androidx.compose.ui.platform.LocalContext.current
    var notifGranted by remember { mutableStateOf(androidx.core.app.NotificationManagerCompat.getEnabledListenerPackages(context).contains(context.packageName)) }
    var adminGranted by remember { mutableStateOf(
        (context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager)
        .isAdminActive(android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java))
    ) }
    var accessGranted by remember { mutableStateOf(
        try {
            android.provider.Settings.Secure.getInt(context.contentResolver, android.provider.Settings.Secure.ACCESSIBILITY_ENABLED) == 1
        } catch (e: Exception) { false }
    ) }
    var overlayGranted by remember { mutableStateOf(android.provider.Settings.canDrawOverlays(context)) }

    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(1000)
        notifGranted = androidx.core.app.NotificationManagerCompat.getEnabledListenerPackages(context).contains(context.packageName)
        adminGranted = (context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager)
            .isAdminActive(android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java))
        accessGranted = try {
            android.provider.Settings.Secure.getInt(context.contentResolver, android.provider.Settings.Secure.ACCESSIBILITY_ENABLED) == 1
        } catch (e: Exception) { false }
        overlayGranted = android.provider.Settings.canDrawOverlays(context)
    }"""

content = re.sub(r'    val context = androidx\.compose\.ui\.platform\.LocalContext\.current\n    var notifGranted by remember \{ mutableStateOf\(false\) \}\n    var adminGranted by remember \{ mutableStateOf\(false\) \}\n    var accessGranted by remember \{ mutableStateOf\(false\) \}\n    var overlayGranted by remember \{ mutableStateOf\(false\) \}', replacement, content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
