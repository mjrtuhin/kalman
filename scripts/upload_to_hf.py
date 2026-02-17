"""
Upload trained model to Hugging Face Hub.
"""

from huggingface_hub import HfApi, create_repo, upload_file
import os

print("="*70)
print("KALMAN - Upload Model to Hugging Face Hub")
print("="*70)

api = HfApi()

print("\n📝 You need a Hugging Face account and token.")
print("   1. Go to: https://huggingface.co/settings/tokens")
print("   2. Create a 'Write' token")
print("   3. Copy the token")
print()

token = input("Paste your HF token (or press Enter to skip): ").strip()

if not token:
    print("\n⚠️  Skipping upload - no token provided")
    print("   Model saved locally at: models/house_2024_improved_v1.cbm")
    print("   You can upload manually later")
    exit(0)

repo_name = input("\nRepository name (e.g., 'kalman-models'): ").strip() or "kalman-models"

username = api.whoami(token=token)["name"]
repo_id = f"{username}/{repo_name}"

print(f"\n📦 Creating repository: {repo_id}")

try:
    create_repo(repo_id=repo_id, token=token, repo_type="model", exist_ok=True)
    print(f"✅ Repository created/exists")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print(f"\n📤 Uploading model file...")

try:
    upload_file(
        path_or_fileobj="models/house_2024_improved_v1.cbm",
        path_in_repo="house_2024_improved_v1.cbm",
        repo_id=repo_id,
        token=token
    )
    print(f"✅ Model uploaded")
    
    upload_file(
        path_or_fileobj="models/house_2024_improved_v1_metadata.json",
        path_in_repo="house_2024_improved_v1_metadata.json",
        repo_id=repo_id,
        token=token
    )
    print(f"✅ Metadata uploaded")
    
    print(f"\n🎉 Success!")
    print(f"   View at: https://huggingface.co/{repo_id}")
    
except Exception as e:
    print(f"❌ Upload failed: {e}")
