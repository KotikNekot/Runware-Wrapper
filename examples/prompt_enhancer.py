from asyncio import run

from pyrunware import RunwareWS


async def main():
    runware = RunwareWS("<token>")

    await runware.start()

    prompts = await runware.prompt_enhancer(
        prompt="pixel cat",
        prompt_max_length=400,
        amount_results=5
    )

    for prompt in prompts:
        print(prompt.text)

    await runware.stop()


run(main())