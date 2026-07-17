import re

with open('.github/workflows/build.yml', 'r') as f:
    content = f.read()

# Add a step to fix google-services.json
replacement = """    - name: Setup google-services.json
      run: |
        if [ ! -f app/google-services.json ]; then
          echo '{"project_info":{"project_number":"123","project_id":"dummy","storage_bucket":"dummy"},"client":[{"client_info":{"mobilesdk_app_id":"1:123:android:abc","android_client_info":{"package_name":"com.yash.synccontrol"}},"oauth_client":[],"api_key":[{"current_key":"dummy"}],"services":{"appinvite_service":{"other_platform_oauth_client":[]}}}]}' > app/google-services.json
        else
          sed -i 's/com.example/com.yash.synccontrol/g' app/google-services.json
        fi

    - name: Generate debug.keystore if missing"""

content = content.replace("    - name: Generate debug.keystore if missing", replacement)

with open('.github/workflows/build.yml', 'w') as f:
    f.write(content)
