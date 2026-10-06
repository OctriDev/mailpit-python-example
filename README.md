# Mailpit Python SDK example

[![SDK Quality](https://github.com/OctriDev/mailpit-python-example/actions/workflows/sdk-quality.yml/badge.svg)](https://github.com/OctriDev/mailpit-python-example/actions/workflows/sdk-quality.yml)
[![Consumer and live API](https://github.com/OctriDev/mailpit-python-example/actions/workflows/example-acceptance.yml/badge.svg)](https://github.com/OctriDev/mailpit-python-example/actions/workflows/example-acceptance.yml)

A complete, unofficial Python client for the [Mailpit email testing API](https://mailpit.axllent.org/docs/api-v1/), generated through [Octri production](https://octri.dev). All 25 operations are included. The example captures an email locally, finds it in the inbox and search results, and retrieves its text, HTML, and original attachment bytes.

Requires **Python 3.10+**. Node.js 20+ is also needed for the generated mock tests. Mailpit captures the example email locally.

## Try it

Start Mailpit in another terminal:

```sh
docker run --rm -p 127.0.0.1:8025:8025 -p 127.0.0.1:1025:1025 axllent/mailpit:v1.31.4
```

Run the checked-in [example](examples/quickstart.py):

```sh
git clone https://github.com/OctriDev/mailpit-python-example.git
cd mailpit-python-example
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
python examples/quickstart.py
```

The command prints the captured message ID after checking send, list, search, nullable recipient fields, text, HTML, and binary retrieval. Open [the Mailpit inbox](http://localhost:8025) to inspect the email. Set `MAILPIT_BASE_URL` to use a different local Mailpit instance.

## Use the SDK

Install the wheel from the [v1.0.0 release](https://github.com/OctriDev/mailpit-python-example/releases/tag/v1.0.0), or run `python -m pip install git+https://github.com/OctriDev/mailpit-python-example.git@v1.0.0`. Import `Mailpit` and `ClientConfig` from `octri_mailpit_example`. Models use Pydantic and the package includes `py.typed`.

The client groups methods under `application`, `message`, `messages`, `tags`, `testing`, and `other` (namespace names use lowercase). Generated models, request options, retry controls, typed errors, and response metadata are included. [sdk-manifest.json](sdk-manifest.json) lists every operation and its wire contract.

## Verify it

The generated [SDK Quality workflow](.github/workflows/sdk-quality.yml) runs formatting, lint/static analysis, compilation, native/mock tests, and packaging. The additional [consumer workflow](.github/workflows/example-acceptance.yml) installs the built package into a clean consumer and runs the example against pinned Mailpit. Failures block their jobs.

With the development tools installed and Mailpit running:

```sh
python -m pip install '.[dev]' build
./scripts/test
./scripts/check-example
```

[VALIDATION.md](VALIDATION.md) records the local checks and coverage limits. Published CI verifies the exact repository commit.

## Generation and source

[generation.json](generation.json) records the production endpoint, project, build, source hashes, and artifact hash. The [original Swagger spec](spec/mailpit.swagger.json) is pinned to Mailpit v1.31.4. [spec/openapi.json](spec/openapi.json) is the exact input sent to production.

The preparation script makes three documented adjustments: it declares the nullable summary recipient arrays observed in Mailpit, gives the send response a named model to avoid Octri's current TypeScript inline-response decoding limitation, and preserves operation media types during Swagger conversion. Binary responses are explicitly marked as binary. All 25 operations remain included; generated SDK implementation files receive formatter changes only.

Reproduce the input without API credentials:

```sh
cd spec
npm ci
node prepare-spec.mjs
git diff --exit-code -- openapi.json
```

This is an Octri example, independently maintained and unaffiliated with Mailpit. See [LICENSE](LICENSE) for the SDK license and [spec/UPSTREAM-LICENSE](spec/UPSTREAM-LICENSE) for the source-spec license.
