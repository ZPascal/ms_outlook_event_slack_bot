import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    coverage_string: str = "![Coverage report](https://github.com/ZPascal/ms_outlook_event_slack_bot/blob/main/docs/coverage.svg)"
    long_description: str = fh.read()

long_description = long_description.replace(coverage_string, "")

setuptools.setup(
    name="outlook-event-slack-bot",
    version="0.0.5",
    author="Pascal Zimmermann",
    author_email="info@theiotstudio.com",
    description="A Microsoft Outlook event Slack bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZPascal/ms_outlook_event_slack_bot",
    project_urls={
        "Source": "https://github.com/ZPascal/ms_outlook_event_slack_bot",
        "Bug Tracker": "https://github.com/ZPascal/ms_outlook_event_slack_bot/issues",
        "Documentation": "https://zpascal.github.io/ms_outlook_event_slack_bot/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    packages=["outlook_event_slack_notification_bot"],
    install_requires=["httpx[http2]", "msal"],
    tests_require=["pytest-httpx", "pytest"],
    python_requires=">=3.8",
)
