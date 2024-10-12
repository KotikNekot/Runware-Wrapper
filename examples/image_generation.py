from asyncio import run

from pyrunware import RunwareWS


async def main():
    runware = RunwareWS("<token>")

    await runware.start()

    images = await runware.image_inference(
        positive_prompt="pixel cat",
        model="runware:100@1",
    )

    for image in images:
        print(image.image_url)

    await runware.stop()


run(main())