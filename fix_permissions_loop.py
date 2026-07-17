import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

replacement = """    androidx.compose.runtime.LaunchedEffect(Unit) {
        while(true) {
            notifGranted = androidx.core.app.NotificationManagerCompat.getEnabledListenerPackages(context).contains(context.packageName)
            adminGranted = (context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager)
                .isAdminActive(android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java))
            accessGranted = try {
                android.provider.Settings.Secure.getInt(context.contentResolver, android.provider.Settings.Secure.ACCESSIBILITY_ENABLED) == 1
            } catch (e: Exception) { false }
            overlayGranted = android.provider.Settings.canDrawOverlays(context)
            kotlinx.coroutines.delay(1000)
        }
    }"""

content = re.sub(r'    androidx\.compose\.runtime\.LaunchedEffect\(Unit\) \{\n        kotlinx\.coroutines\.delay\(1000\)\n[\s\S]*?        overlayGranted = android\.provider\.Settings\.canDrawOverlays\(context\)\n    \}', replacement, content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
