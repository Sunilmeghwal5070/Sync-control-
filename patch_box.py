import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = "androidx.compose.foundation.layout.Box(modifier = Modifier.padding(innerPadding)) {"
replacement = "androidx.compose.foundation.layout.Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
