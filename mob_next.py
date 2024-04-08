import os
import subprocess


def mob_next(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            path = os.path.join(root, name)
            result = subprocess.run(["mob", "status"], capture_output=True, text=True, cwd=path)
            print(path)
            if "you are on wip branch mob" in result.stdout:
                print("yes")
            else:
                print("no")

        break

mob_next("/home/vittorioguerriero/repos")
