import re
files = ['app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'app/src/main/java/com/example/services/MyNotificationListenerService.kt']

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    if 'import kotlinx.coroutines.flow.first' not in content:
        content = content.replace("import kotlinx.coroutines.flow.MutableStateFlow", "import kotlinx.coroutines.flow.MutableStateFlow\nimport kotlinx.coroutines.flow.first")
        with open(file, 'w') as f:
            f.write(content)
