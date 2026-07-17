#!/bin/bash
sed -i 's/RestrictionsScreen(/val config by viewModel.deviceConfig.collectAsStateWithLifecycle()\n            RestrictionsScreen(\n                deviceConfig = config,\n                onConfigChanged = { viewModel.updateConfig(it) },/' app/src/main/java/com/example/navigation/AppNavigation.kt
