import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """fun ChildDashboard(
    pairCode: String,
    deviceConfig: com.example.data.DeviceConfig,
    onSendMockNotification: (String, String) -> Unit,
    onDisconnect: () -> Unit
) {"""
replacement = """import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items

fun ChildDashboard(
    pairCode: String,
    deviceConfig: com.example.data.DeviceConfig,
    onSendMockNotification: (String, String) -> Unit,
    onUpdateAppStatus: (List<com.example.data.AppInfo>) -> Unit,
    onDisconnect: () -> Unit
) {"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
