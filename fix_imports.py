with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.lazy.items\n\nfun ChildDashboard", "fun ChildDashboard")

if "import androidx.compose.foundation.lazy.LazyColumn" not in content:
    content = content.replace("package com.example.ui.screens", "package com.example.ui.screens\n\nimport androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.lazy.items\n")

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
