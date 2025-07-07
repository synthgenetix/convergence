# Convergence Tasks

1. Implement `/transcribe` using Open AI. Should include FastAPI endpoint and library methods. Manually test the endpoint and library calls. Make sure it's stateless.

2. Create live documentation page. Try ReDoc or GitBook. If we can self-host the Swagger docs, that will be good too. But let's not use Swagger, and use something more aesthetic and modern.

3. Publish package to pip. Do a fresh install and see if everything is working properly. Test for system dependencies, and see if we can test on Linux and Windows VM or VM machine too. Ensure a consistent experience across Operating Systems and document the setup instructions for each. Create a clear compatability and system requirements section in the README. Add necessary publish scripts.

4. Move documentation out of `README.md` into a separate documentation file: `SETUP.md`, `API_USAGE.md`, `SDK_USAGE.md`, `FEATURES.md`, `DEV_SETUP.md`, `SELF_HOST.md`, `CONTRIBUTIONS.md` and `API_KEY_MANAGEMENT.md` files in the docs folder.

5. Fix duration handling in the audio. For example, passing duration as 5 mins led to a conversation of just 2 minutes. This discrepancy in the duration can cause problems to users who care about time-sensitive audio files. Consider adding `time_detection(audio_file: List[Byte]) -> int` functionality to detect the time of an audio segment — a section of the conversation with distinct start and end spoken by the user.
