import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = "LazyColumn {"
replacement = "LazyColumn(modifier = Modifier.heightIn(max = 300.dp)) {"
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
