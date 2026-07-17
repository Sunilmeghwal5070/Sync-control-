with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

if "import kotlinx.coroutines.channels.awaitClose" not in content:
    content = content.replace("package com.example.viewmodel", "package com.example.viewmodel\n\nimport kotlinx.coroutines.channels.awaitClose\nimport kotlinx.coroutines.tasks.await")

content = content.replace("kotlinx.coroutines.channels.awaitClose", "awaitClose")
content = content.replace("kotlinx.coroutines.tasks.await", "await")

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
