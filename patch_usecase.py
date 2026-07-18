import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target1 = """fun UseCaseScreen(
    pairedDevice: PairedDevice?,
    hasParentRole: Boolean,
    viewModel: AppViewModel,
    onNavigateToRoleSelection: () -> Unit,
    onNavigateToParentDashboard: () -> Unit,
    onDisconnect: () -> Unit
) {"""
replacement1 = """fun UseCaseScreen(
    pairedDevice: PairedDevice?,
    hasParentRole: Boolean,
    viewModel: AppViewModel,
    onNavigateToRole: (String) -> Unit,
    onNavigateToParentDashboard: () -> Unit,
    onDisconnect: () -> Unit
) {"""
content = content.replace(target1, replacement1)

target2 = """            Spacer(modifier = Modifier.height(16.dp))
            Text("What's Your Use Case?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(32.dp))
            
            UseCaseCard(title = "Parent / Child", onClick = onNavigateToRoleSelection)
            
            Spacer(modifier = Modifier.weight(1f))"""
replacement2 = """            Spacer(modifier = Modifier.height(16.dp))
            Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(48.dp))
            
            UseCaseCard(title = "Parent", onClick = { onNavigateToRole("parent") })
            Spacer(modifier = Modifier.height(32.dp))
            UseCaseCard(title = "Child", onClick = { onNavigateToRole("child") })
            
            Spacer(modifier = Modifier.weight(1f))"""
content = content.replace(target2, replacement2)

target_role_selection = """fun RoleSelectionScreen(onRoleSelected: (String) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        
        Spacer(modifier = Modifier.height(48.dp))
        
        UseCaseCard(title = "Parent", onClick = { onRoleSelected("parent") })
        Spacer(modifier = Modifier.height(32.dp))
        UseCaseCard(title = "Child", onClick = { onRoleSelected("child") })
    }
}"""
content = content.replace(target_role_selection, "")

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
