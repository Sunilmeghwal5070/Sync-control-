import re
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()
target = """data class AppInfo(
    val packageName: String = "",
    val appName: String = "",
    val isLocked: Boolean = false,
    val isHidden: Boolean = false
)"""
replacement = """data class AppInfo(
    val packageName: String = "",
    val appName: String = "",
    val isLocked: Boolean = false,
    val isHidden: Boolean = false,
    val notificationsEnabled: Boolean = true
)"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)
