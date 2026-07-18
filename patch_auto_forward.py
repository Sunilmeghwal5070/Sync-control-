import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """    // Auto-proceed if all granted, but user can also click continue manually
    androidx.compose.runtime.LaunchedEffect(allGranted) {
        if (allGranted) {
            onPermissionsGranted()
        }
    }"""
replacement = """    // Removed auto-proceed so user can navigate back without getting trapped"""
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
