#!/bin/bash
sed -i 's/val intent = android.content.Intent(android.provider.Settings.ACTION_SECURITY_SETTINGS)/val intent = android.content.Intent(android.app.admin.DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN).apply { putExtra(android.app.admin.DevicePolicyManager.EXTRA_DEVICE_ADMIN, android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java)) }/g' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i 's/notifGranted = true//g' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i 's/adminGranted = true//g' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i 's/accessGranted = true//g' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i 's/overlayGranted = true//g' app/src/main/java/com/example/ui/screens/MainScreens.kt
