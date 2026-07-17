import re

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

# 1. Fix auto-skip permissions
replacement_skip = """    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState.allPermissionsGranted && cameraPermissionState.allPermissionsGranted && overlayGranted
    var showWarning by remember { mutableStateOf(false) }

    androidx.compose.runtime.LaunchedEffect(allGranted) {
        if (allGranted) {
            onPermissionsGranted()
        }
    }"""

content = re.sub(r'    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState\.allPermissionsGranted && cameraPermissionState\.allPermissionsGranted && overlayGranted\n    var showWarning by remember \{ mutableStateOf\(false\) \}', replacement_skip, content)


# 2. Fix text: if (role == "child") -> if (role == "parent") for "Get Child's Notification"
content = content.replace(
    'Text(if (role == "child") "Get Child\'s Notification" else "Share Notification"',
    'Text(if (role == "parent") "Get Child\'s Notification" else "Share Notification"'
)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
