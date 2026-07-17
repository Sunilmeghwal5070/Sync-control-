with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("import awaitClose", "import kotlinx.coroutines.channels.awaitClose")
content = content.replace("import await", "import kotlinx.coroutines.tasks.await")

with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
