from asyncio import run

from pyrunware import RunwareWS


async def main():
    runware = RunwareWS("<token>")

    await runware.start()

    image = await runware.remove_background(
        image="https://im.runware.ai/image/ws/0.5/ii/4ef5758a-acce-4f0b-9691-064fbdbc2441.jpg",
    )
    print(image.image_url)

    await runware.stop()


run(main())