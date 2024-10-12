from asyncio import run

from pyrunware import RunwareWS


async def main():
    runware = RunwareWS("<token>")

    await runware.start()

    image = await runware.upscale(
        image="https://im.runware.ai/image/ws/0.5/ii/0c8492c6-a241-42fa-bba9-3e92851305c8.jpg",
        upscale_factor=4
    )

    print(image.image_url)

    await runware.stop()


run(main())