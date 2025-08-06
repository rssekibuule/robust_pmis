#!/usr/bin/env python3
"""
Verify Models Script - Check if our models are available
"""

import subprocess
import sys
import os
import tempfile

def create_verification_script():
    """Create the verification script"""
    
    script_content = '''
print("🔍 Verifying Models...")

# Check available models
try:
    print("📋 Available models:")
    all_models = list(env.registry.keys())
    kcca_models = [m for m in all_models if 'kcca' in m or 'programme' in m or 'piap' in m]
    
    print(f"🎯 KCCA/Programme related models ({len(kcca_models)}):")
    for model in sorted(kcca_models):
        print(f"   • {model}")
    
    # Try to access specific models
    print("\\n🔍 Testing model access:")
    
    # Test programme model
    try:
        programmes = env['kcca.programme'].search([])
        print(f"✅ kcca.programme: Found {len(programmes)} records")
        if programmes:
            print(f"   📋 Sample: {programmes[0].name}")
    except Exception as e:
        print(f"❌ kcca.programme: {e}")
    
    # Test piap.action model
    try:
        piap_actions = env['piap.action'].search([])
        print(f"✅ piap.action: Found {len(piap_actions)} records")
    except Exception as e:
        print(f"❌ piap.action: {e}")
    
    # Test other models
    for model_name in ['programme.objective', 'intermediate.outcome', 'intervention', 'output']:
        try:
            records = env[model_name].search([])
            print(f"✅ {model_name}: Found {len(records)} records")
        except Exception as e:
            print(f"❌ {model_name}: {e}")
    
except Exception as e:
    print(f"❌ Error during verification: {e}")
    import traceback
    traceback.print_exc()

print("\\n🎉 Verification Complete!")
exit()
'''
    
    return script_content

def run_verification():
    """Run the verification using Odoo shell"""
    
    print("🔍 Starting Model Verification...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_verification_script())
        script_path = f.name
    
    try:
        # Change to the correct directory
        os.chdir('/home/richards/Dev/odoo18/addons/robust_pmis')
        
        # Run odoo shell with our script
        cmd = [
            'python3', '/home/richards/Dev/odoo18/odoo-bin', 
            'shell', 
            '-d', 'test_db',
            '--addons-path=/home/richards/Dev/odoo18/addons'
        ]
        
        print(f"🔧 Command: {' '.join(cmd)}")
        
        # Execute the verification script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the verification commands
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        stdout, stderr = process.communicate(input=script_content)
        
        print('📤 STDOUT:')
        print(stdout)
        if stderr:
            print('⚠️ STDERR:')
            print(stderr)
        print(f'🔄 Return code: {process.returncode}')
        
        return process.returncode == 0
        
    finally:
        # Clean up temporary file
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == "__main__":
    success = run_verification()
    if success:
        print("\\n🎉 Verification completed successfully!")
    else:
        print("\\n❌ Verification failed!")
        sys.exit(1)
