import asyncio
from desktop_notifier import DesktopNotifier, Icon

import config





def simple(title, message):
    notifier = DesktopNotifier()

    async def main():
        await notifier.send(title=title, message=message)

    asyncio.run(main())
