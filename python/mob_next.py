import os
import subprocess


class MobNext:
    def __init__(self, handler, paths):
        self.handler = handler
        self.paths = paths

    @classmethod
    async def create(cls, handler, paths):
        mob_next = MobNext(handler, paths)

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
                            print(f"Found mob branch with changes in {path}")
                            mob_next_result = self.run_mob_next(path)
                            print(mob_next_result.stdout)
                            await self.handler.on_end()
                            return

                break

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
