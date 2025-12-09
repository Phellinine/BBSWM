import asyncio
from desktop_notifier import DesktopNotifier, Icon

import config





def simple(title, message):
    notifier = DesktopNotifier()

    async def main():
        await notifier.send(title=message, message=title)

    asyncio.run(main())
