import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

content = re.sub(r'@Composable\s*@OptIn\(com\.google\.accompanist\.permissions\.ExperimentalPermissionsApi::class\)\s*@Composable',
                 r'@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\n@Composable',
                 content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
