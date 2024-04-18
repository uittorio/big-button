import os
import subprocess
import re


class MobNext:
    def __init__(self, handler, paths, verbose=True):
        self.handler = handler
        self.paths = paths
        if verbose:
            self.printer = VerboseMobNextPrinter()
        else:
            self.printer = SilentMobNextPrinter()

    @classmethod
    async def create(cls, handler, paths, verbose):
        mob_next = MobNext(handler, paths, verbose)

        def _run_cb():
            async def __run():
                await mob_next._run()
            return __run

        await handler.on_notify(_run_cb())
        return mob_next

    async def _run(self):
        await self.handler.on_start()
        for directory in self.paths:
            for root, dirs, files in os.walk(directory):
                for name in dirs:
                    path = os.path.join(root, name)
                    mob_status_result = self.run_mob_status(path)
                    if "you are on wip branch mob" in mob_status_result.stdout:
                        git_status_result = self.run_git_status(path)
                        if "nothing to commit, working tree clean" not in git_status_result.stdout:
                            self.printer.print_mob_branch_found(path)
                            mob_next_result = self.run_mob_next(path)
                            self.printer.print_mob_next_done(mob_next_result.stdout)
                            await self.handler.on_end()
                            return

                break

        self.printer.print_no_mob_branches_found()
        await self.handler.on_end()

    @staticmethod
    def run_mob_status(path):
        return subprocess.run(["mob", "status"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_git_status(path):
        return subprocess.run(["git", "status"], capture_output=True, text=True, cwd=path)

    @staticmethod
    def run_mob_next(path):
        return subprocess.run(["mob", "next"], capture_output=True, text=True, cwd=path)


class VerboseMobNextPrinter:
    @staticmethod
    def print_no_mob_branches_found():
        print("Found no mob branches with changes, skipping")

    @staticmethod
    def print_mob_branch_found(path: str):
        print(f"Found mob branch with changes in {path}")

    @staticmethod
    def print_mob_next_done(mob_next_result: str):
        print(mob_next_result)


class SilentMobNextPrinter:
    @staticmethod
    def print_no_mob_branches_found():
        print("X")

    @staticmethod
    def print_mob_branch_found(path):
        print(f"@ {path}")

    @staticmethod
    def print_mob_next_done(mob_next_result: str):
        print(f"# {SilentMobNextPrinter.extract_next_person(mob_next_result)}")

    @staticmethod
    def extract_next_person(mob_next_result):
        match = re.search(r'\*\*\*(.*?)\*\*\*', mob_next_result)
        if match:
            return f"-> {match.group(1)}"
        return "No partner found"

