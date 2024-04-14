import os
import subprocess


def mob_next(paths):
    for directory in paths:
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                path = os.path.join(root, name)
                mob_status_result = run_mob_status(path)
                if "you are on wip branch mob" in mob_status_result.stdout:
                    git_status_result = run_git_status(path)
                    if "nothing to commit, working tree clean" not in git_status_result.stdout:
                        print(f"Found mob branch with changes in {path}")
                        mob_next_result = run_mob_next(path)
                        print(mob_next_result.stdout)
                        return

            break


def run_mob_status(path):
    return subprocess.run(["mob", "status"], capture_output=True, text=True, cwd=path)


def run_git_status(path):
    return subprocess.run(["git", "status"], capture_output=True, text=True, cwd=path)


def run_mob_next(path):
    return subprocess.run(["mob", "next"], capture_output=True, text=True, cwd=path)