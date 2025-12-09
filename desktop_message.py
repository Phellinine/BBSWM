import asyncio
from desktop_notifier import DesktopNotifier, Icon

import config


# notifier = DesktopNotifier()


def simple(title, message):
    notifier = DesktopNotifier()

    async def main():
        await notifier.send(title=message, message=title, icon=Icon(uri=config.icon_path))

    asyncio.run(main())
