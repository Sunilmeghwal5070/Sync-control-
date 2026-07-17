#!/bin/bash
sed -i 's/val intent = android.content.Intent(android.provider.Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS).*/val intent = android.content.Intent(android.provider.Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)\n                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available", android.widget.Toast.LENGTH_SHORT).show(); notifGranted = true }/g' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i '/try {/,/}/d' app/src/main/java/com/example/ui/screens/MainScreens.kt
