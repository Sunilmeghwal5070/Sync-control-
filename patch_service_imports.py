import re
with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.tasks.await", "import kotlinx.coroutines.tasks.await\nimport kotlinx.coroutines.flow.first")

with open('app/src/main/java/com/example/services/MyNotificationListenerService.kt', 'w') as f:
    f.write(content)
