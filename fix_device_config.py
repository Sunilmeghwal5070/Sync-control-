import re

with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()

replacement = """    val location: LocationData = LocationData(0.0, 0.0),
    val installedApps: List<AppInfo> = emptyList(),
    val pairingRequested: Boolean = false,
    val pairingAccepted: Boolean = false
)"""

content = re.sub(r'    val location: LocationData = LocationData\(0\.0, 0\.0\),\n    val installedApps: List<AppInfo> = emptyList\(\)\n\)', replacement, content)

with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)
