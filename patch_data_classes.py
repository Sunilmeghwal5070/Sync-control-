import re
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()

data_classes = """data class DeviceConfig(
    val wifi: Boolean = false,
    val bluetooth: Boolean = false,
    val flashlight: Boolean = false,
    val hotspot: Boolean = false,
    val ringerMode: Int = 2, // 0 = silent, 1 = vibrate, 2 = normal
    val volume: Int = 50,
    val brightness: Int = 100,
    val lock: Boolean = false,
    val aeroplaneMode: Boolean = false,
    val screenshotRequested: Boolean = false,
    val batterySaver: Boolean = false,
    val dndMode: Boolean = false,
    val screenTimeout: Int = 30,
    val cameraAccess: Boolean = true,
    val microphoneAccess: Boolean = true,
    val batteryLevel: Int = 85,
    val location: LocationData = LocationData(0.0, 0.0),
    val installedApps: List<AppInfo> = emptyList(),
    val pairingRequested: Boolean = false,
    val pairingAccepted: Boolean = false
)

data class LocationData(val lat: Double = 0.0, val lng: Double = 0.0)

data class AppInfo(
    val packageName: String = "",
    val appName: String = "",
    val isLocked: Boolean = false,
    val isHidden: Boolean = false,
    val notificationsEnabled: Boolean = true
)

"""
if "data class DeviceConfig" not in content:
    content = content.replace("object MockDatabase", data_classes + "object MockDatabase")
    with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
        f.write(content)
