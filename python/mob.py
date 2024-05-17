import os
import subprocess
import re


class Mob:
    def __init__(self, paths, verbose=True):
        self.paths = paths
        if verbose:
            self.printer = VerboseMobNextPrinter()
        else:
            self.printer = SilentMobNextPrinter()

    @classmethod
    def create(cls, paths, verbose):
        mob_next = Mob(paths, verbose)
        return mob_next

    async def list_mob_branches(self):
        for directory in self.paths:
            for root, dirs, files in os.walk(directory):
                for name in dirs:
                    path = os.path.join(root, name)
                    mob_status_result = self.run_mob_status(path)
                    if "you are on wip branch mob" in mob_status_result.stdout:
                        git_status_result = self.run_git_status(path)
                        if "nothing to commit, working tree clean" not in git_status_result.stdout:
                            self.printer.print_mob_branch_with_changes_found(path)

                break

    async def next(self):
        self.printer.print_mob_next_begin()
        for directory in self.paths:
            for root, dirs, files in os.walk(directory):
                for name in dirs:
                    path = os.path.join(root, name)
                    mob_status_result = self.run_mob_status(path)
                    if "you are on wip branch mob" in mob_status_result.stdout:
                        git_status_result = self.run_git_status(path)
                        if "nothing to commit, working tree clean" not in git_status_result.stdout:
                            self.printer.print_mob_branch_with_changes_found(path)
                            mob_next_result = self.run_mob_next(path)
                            self.printer.print_mob_next_done(mob_next_result.stdout)
                            return

                break

        self.printer.print_no_mob_branches_with_changes_found()

    async def start(self):
        self.printer.print_mob_start_begin()
        for directory in self.paths:
            for root, dirs, files in os.walk(directory):
                for name in dirs:
                    path = os.path.join(root, name)
                    mob_status_result = self.run_mob_status(path)
                    if "you are on wip branch mob" in mob_status_result.stdout:
                        self.run_git_remote_update(path)
                        git_status_result = self.run_git_status(path)
                        if "nothing to commit, working tree clean" in git_status_result.stdout:
                            if "branch is up-to-date with" not in git_status_result.stdout:
                                self.printer.print_mob_branch_behind_found(path)
                                mob_next_result = self.run_mob_start(path)
                                self.printer.print_mob_start_done(mob_next_result.stdout)
                                return

                break

        self.printer.print_no_mob_branches_behind_found()

    @staticmethod
    def run_mob_status(path):
        return subprocess.run(["mob", "status"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_git_status(path):
        return subprocess.run(["git", "status"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_git_remote_update(path):
        return subprocess.run(["git", "remote", "update"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_mob_next(path):
        return subprocess.run(["mob", "next"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_mob_start(path):
        return subprocess.run(["mob", "start"], capture_output=True, text=True, cwd=path)


class VerboseMobNextPrinter:
    @staticmethod
    def print_no_mob_branches_with_changes_found():
        print("Found no mob branches with changes, skipping")

    @staticmethod
    def print_no_mob_branches_behind_found():
        print("Found no mob branches behind, skipping")

    @staticmethod
    def print_mob_branch_with_changes_found(path):
        print(f"Found mob branch with changes in {path}")

    @staticmethod
    def print_mob_branch_behind_found(path):
        print(f"Found mob branch behind in {path}")

    @staticmethod
    def print_mob_next_begin():
        print("mob next")

    @staticmethod
    def print_mob_next_done(mob_next_result: str):
        print(mob_next_result)

    @staticmethod
    def print_mob_start_begin():
        print("mob start")

    @staticmethod
    def print_mob_start_done(mob_start_result: str):
        print(mob_start_result)


class SilentMobNextPrinter:
    @staticmethod
    def print_no_mob_branches_with_changes_found():
        print("X")

    @staticmethod
    def print_no_mob_branches_behind_found():
        print("X")

    @staticmethod
    def print_mob_branch_with_changes_found(path):
        print(f"{path}")

    @staticmethod
    def print_mob_branch_behind_found(path):
        print(f"{path}")

    @staticmethod
    def print_mob_next_begin():
        print("↑ ", end="", flush=True)

    @staticmethod
    def print_mob_next_done(mob_next_result: str):
        print(f"# {SilentMobNextPrinter.extract_next_person(mob_next_result)}")

    @staticmethod
    def extract_next_person(mob_next_result):
        match = re.search(r'\*\*\*(.*?)\*\*\*', mob_next_result)
        if match:
            return f"-> {match.group(1)}"
        return "No partner found"

    @staticmethod
    def print_mob_start_begin():
        print("↓ ", end="", flush=True)

    @staticmethod
    def print_mob_start_done(_: str):
        print("✓")

