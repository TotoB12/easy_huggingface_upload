import os
from huggingface_hub import HfApi, Repository
import shutil

def upload_video_to_huggingface(video_path, dataset_name, token):
    api = HfApi()
  
    dataset_repo_name = f"TotoB12/{dataset_name}"

    clone_url = api.create_repo(
        repo_id=dataset_repo_name,
        token=token,
        repo_type="dataset",
        private=False,
        exist_ok=True
    )

    repo_local_path = os.path.join(os.path.dirname(__file__), dataset_name)

    repo = Repository(repo_local_path, clone_from=clone_url, use_auth_token=token)

    video_filename = os.path.basename(video_path)
    repo_video_path = os.path.join(repo_local_path, video_filename)
    os.makedirs(os.path.dirname(repo_video_path), exist_ok=True)
    shutil.copy(video_path, repo_video_path)

    repo.git_add(auto_lfs_track=True)
    repo.git_commit(f"Upload video file: {video_filename}")
    repo.git_push()

    print(f"Video {video_filename} uploaded successfully to dataset {dataset_name} on Hugging Face.")

if __name__ == "__main__":
    video_path = input("Enter the path to your video file: ")
    
    dataset_name = input("Enter your Hugging Face Dataset name: ")
    
    token = input("Enter your Hugging Face authentication token: ")
    
    upload_video_to_huggingface(video_path, dataset_name, token)
