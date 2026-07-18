import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target2 = """            Text("What's Your Use Case?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(32.dp))
            
            UseCaseCard(title = "Parent / Child", onClick = onNavigateToRoleSelection)
            Spacer(modifier = Modifier.height(24.dp))
            Spacer(modifier = Modifier.weight(1f))"""
replacement2 = """            Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(48.dp))
            
            UseCaseCard(title = "Parent", onClick = { onNavigateToRole("parent") })
            Spacer(modifier = Modifier.height(32.dp))
            UseCaseCard(title = "Child", onClick = { onNavigateToRole("child") })
            
            Spacer(modifier = Modifier.weight(1f))"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
