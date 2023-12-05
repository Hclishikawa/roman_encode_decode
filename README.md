
# Sample Python Development Project

This is a sample Python development project that uses Python poetry, pytest, coverage and Docker to test and package the code. We also create a software bill of materials (SBOM) for our Docker image and then scan the Docker images for vulnerabilites with Trivy and Grype.

This is meant to be used as a tutorial.

The topics covered will be:

- Poetry: for controlling Python libraries and preventing version conflicts among those libraries. In addition to builing a standardized project framework scaffold.
- Pytest: the use of Pytest to unit test the code.
- Coverage: to insure that we are testing all the code in the code base.
- Using a multi-target Dockerfile to create Test (Development) and Production container images.
- Checkov: to insure that our Dockerfile does not introduce any security vulnerabilities.
- Trivy: to scan our containers for security vulnerabilities.
- Syft: to create a container Software Bill Of Materials (SBOM). A “software bill of materials” (SBOM) has emerged as a key building block in software security and software supply chain risk management. A software Bill of Materials (SBOM) is a list of all the open source and third-party components present in a codebase. A SBOM also lists the licenses that govern those components, the versions of the components used in the codebase, and their patch status, which allows security teams to quickly identify any associated security or license risks.
- Grype: An alternative to Trivy, that can also ingest your SBOM and streamline the scan to make it more efficient.
- Docker commands for some of the various utlities that we will use along with the Windows Docker variation of the commands. Most notably when to use `-v /var/run/docker.sock:/var/run/docker.sock` and `--volume "//var/run/docker.sock:/var/run/docker.sock"`

## Prerequisite: install Poetry

### Linux, macOS, Windows (WSL)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows (Powershell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

See the [Poetry website](https://python-poetry.org/docs/#installation) for more details.

## Prerequisite: install Docker

You will also need Docker on your system.  See [getting started with Docker](https://www.docker.com/get-started/) for more information, if you do not have Docker installed on your system.

You can also use Podman, Rancher, etc. if you desire. You may need to change some of the syntax below to accomodate your environment.

## Setting up the environment

1. Create the directory structure using Poetry for our project "roman_encode_decode". This has already been done. So this step is for illustration purposes only.

```bash
poetry new roman_encode_decode
```

This will create the following directory structure

```bash
roman_encode_decode
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

3. Add this to the toml file (`pyproject.toml`) to create a group called test.  This has already been done. So this step is for illustration purposes only.

```toml
[tool.poetry.group.test]
optional = true

[tool.poetry.group.test.dependencies]
```

4. Let's add the Python library/libraries that we need for the program.  This has already been done. So this step is for illustration purposes only.

```bash
poetry shell
poetry add emoji
```

5. Let's add the Python library/libraries that we need for the program in the **test** environment we created.  This has already been done. So this step is for illustration purposes only.

```bash
poetry add emoji --group test
poetry add coverage --group test
poetry add pytest --group test
poetry add pytest-cov --group test
poetry add pytest-mock --group test
```

6. Let's add the following code to the `pyproject.toml` file to handle some things for Python Coverage.  This has already been done. So this step is for illustration purposes only.

```toml
[tool.coverage.run]
branch = true

[tool.coverage.report]
# Regexes for lines to exclude from consideration
exclude_also = [
    # Don't complain about missing debug-only code:
    "def __repr__",
    "if self\\.debug",

    # Don't complain if tests don't hit defensive assertion code:
    "raise AssertionError",
    "raise NotImplementedError",

    # Don't complain if non-runnable code isn't run:
    "if 0:",
    "if __name__ == .__main__.:",

    # Don't complain about abstract methods, they aren't run:
    "@(abc\\.)?abstractmethod",
    ]

ignore_errors = true

[tool.coverage.html]
directory = "coverage_html_report"

```

7. Execute Poetry Update to get the environment up to date with the toml file.

```bash
poetry update
```

8. Now let's execute Poetry install to put us in the test environment mode.

   ```bash
   poetry install --with test
   ```

9. Run the Python program with Poetry.


```bash
poetry run python roman_encode_decode/main.py
```

11. Let's run the program again using Poetry, PyTest and Coverage to insure that our tests work and that we are testing 100% of our code. NOTE: that the test code usually outnumbers the actual code by a ratio around four to one. This is expected.

```bash
poetry run coverage run --source=roman_encode_decode -m pytest -v tests/ && coverage report -m
```

12. Scan the Dockerfile with the latest version of the checkov container for any security vulnerabilities we might had accidentally coded into the Dockerfile. The below code should be executed in the directory where the Dockerfile resides.

```bash
docker pull bridgecrew/checkov:latest

docker run  --rm --tty --volume $PWD:/tf --workdir /tf bridgecrew/checkov:latest --directory /tf --framework dockerfile > dockerfile_scan_results.txt
```

We should get all the tests marked as passed and one test marked as skipped. The skipped test is for Checkov test CKV_DOCKER_2 where a health check should be installed. Since this is a batch container image there is no reason to install a health check for a load balancer to check, so we added a command `#checkov:skip=CKV_DOCKER_2:Healthcheck is not required for batch images.` to the Dockerfile to skip that test.

If you are running in Windows Git Bash shell in VSCode then use the following command to get around the problem of Git Bash trying to substitute, incorrectly, parts of the `docker run` command.

```bash
MSYS_NO_PATCHCONV=1 docker run  --rm --tty --volume $PWD:/tf --workdir /tf bridgecrew/checkov:latest --directory /tf --framework dockerfile > dockerfile_scan_results.txt
```

13. Build the test docker container of our application. We will tag the container as `test`.

```bash
DOCKER_BUILDKIT=1 docker build --progress auto -t roman_encode_decode:test --target development .
```

Use `--progress plain`   to show itemized container output if you need that level of detail.

14. Use the command `docker image ls` to verify that the image was built.
14. Run the test docker container in interactive mode. This will put us into a Docker bash prompt (interactive terminal).

```bash
docker run --rm -it --name test1 roman_encode_decode:test
```

15. In the interactive terminal on the container run the following commands:

```bash
coverage run --source=roman_encode_decode -m pytest -v tests/ && coverage report -m

python roman_encode_decode/main.py

exit
```

The coverage report will report how much of the code is covered by the test scripts in the `/tests` directory. If you look in the `main.py` script you will see the comment `\# pragma: no cover` next to the main() function. Since the main function in this script acts as a test we tell `pytest` and `coverage` to skip that function and not include it in the coverage calculations.

16. Build the production container and tag it as `prod`.

```bash
DOCKER_BUILDKIT=1 docker build --progress auto -t roman_encode_decode:prod --target production .
```

17. Use the command `docker image ls` to verify that the image was built.

If you notice in your docker console or if you execute `docker image ls` the production container is significantly smaller than the test container.

```bash
docker image ls

REPOSITORY            TAG       IMAGE ID       CREATED        SIZE
roman_encode_decode   prod      2c7f84203015   18 hours ago   271MB
roman_encode_decode   test      4182c4732c7c   23 hours ago   804MB
```

18. Run the production docker container to insure that we get the expected results. (Same as what we got in test.)

```bash
docker run --rm -it --name prod1 roman_encode_decode:prod
```

We should get output like this

```bash
Input:MCMXC Output: 1990
Input:MMVIII Output: 2008
Input:MDCLXVI Output: 1666
Input:lxviv Output: 69
Input: 2 Output: II
Input: 16 Output: XVI
Input: 95 Output: XCV
Input: 242 Output: CCXLII
Input: 575 Output: DLXXV
Input: 1024 Output: MXXIV
Input: 3999 Output: MMMCMXCIX
Input: ['MCMXC', 'IVXLCDM'] Output: True
Input: ['MCMXA', 'IVXLCDM'] Output: False
Input: ['mcmxa', 'IVXLCDM'] Output: False
Input: ['mcmxc', 'IVXLCDM'] Output: False
Input: ['mcmxi', 'ivxlcdm'] Output: True
Input: ['mcmxc', 'ivxlcdm'] Output: True
Done ✅

```

NOTE: To build the production image for another platform such as  arm64, amd64, riscv64, ppc64le, s390x, 386, mips64le, mips64, arm/v7, arm/v6 you can use the following command. **Note**: as long as the base image supports that platform.

```bash
docker buildx build --platform linux/amd64 --progress auto \
-t roman_encode_decode:amd64 --target production . --output type=docker
```

## Container vulnerability scanning

## Docker platform differences

**NOTE**: When using Docker on Windows you will need to translate the volume command (-v, --volume) from   `-v /var/run/docker.sock:/var/run/docker.sock` for Mac and *nix based system to `--volume "//var/run/docker.sock:/var/run/docker.sock"` for Windows based systems.

## Install Trivy

See the [Trivy website for installation instructions for your platform](https://aquasecurity.github.io/trivy/v0.17.2/installation/)

Run Trivy against our production container and save output.

```bash
trivy image roman_encode_decode:prod  > docker_vulnerabiltiy_report.txt
```

To run Trivy as a docker container

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/Library/Caches:/root/.cache/ aquasec/trivy:0.47.0 image roman_encode_decode:prod > docker_vulnerabiltiy_report.txt
```

To run Trivy as a docker container on Windows

```bash
docker run -v "//var/run/docker.sock:/var/run/docker.sock" -v $HOME/Library/Caches:/root/.cache/ aquasec/trivy:0.47.0 image roman_encode_decode:prod > docker_vulnerabiltiy_report.txt
```

As you can see, we have quite a few issues. Many of these are false positives. Trivy has a reputation for producing reports with false positives but you need to be aware of them.

Now let us just run with HIGH and CRITICAL severites.

```bash
trivy image roman_encode_decode:prod --severity "HIGH,CRITICAL" > docker_vulnerabiltiy_report.txt
```

These are the vulnerabilities you need to assess to see if they need to be addressed.

## Install syft

Syft will build a Software Bill Of Materials (SBOM) for your container. This is useful for dealing with IT security if they have questions about what libraries your container is using and for scanning your container with various utilities.

See the [Syft website for installation instructions ](https://github.com/anchore/syft)

```bash
syft roman_encode_decode:prod  > roman_decode_encode_sbom.txt
```

To run the Docker version of Syft in Windows, execute the following commands:

```bash
docker pull registry.gitlab.com/gitlab-ci-utils/container-images/syft:latest

docker run --rm --volume "//var/run/docker.sock:/var/run/docker.sock" \
--name syft registry.gitlab.com/gitlab-ci-utils/container-images/syft:latest \
roman_encode_decode:prod > roman_decode_encode_syft_sbom.txt
```

Now, let's generate a JSON version of the SBOM so we can use it later.

```bash
syft roman_encode_decode:prod -o syft-json > roman_decode_encode_sbom.json
```

To run the Docker version of this command in Windows, execute the following command:

```bash
docker run --rm --volume "//var/run/docker.sock:/var/run/docker.sock" --name syft registry.gitlab.com/gitlab-ci-utils/container-images/syft:latest roman_encode_decode:prod -o syft-json > roman_decode_encode_syft_sbom.json
```

If you need an even more detailed report for all the layers in the container you can use the `--scope` option

```bash
syft roman_encode_decode:prod --scope all-layers > roman_decode_encode_all_layers_bom.txt
```

## Run Grype

Grype is another vulnerability scanner that also can use the Syft BOM file you just produced to speed up the scanning process. For our demonstration, we will just run Grype on the container.

```bash
docker run --rm \
--volume /var/run/docker.sock:/var/run/docker.sock \
--name grype anchore/grype:latest \
 roman_encode_decode:prod  > roman_decode_encode_grype_report.txt
```

If you are running Docker in Windows then use the following command:

```bash
docker run --rm \
--volume "//var/run/docker.sock:/var/run/docker.sock" \
--name grype anchore/grype:latest \
 roman_encode_decode:prod  > roman_decode_encode_grype_report.txt
```

Now, let's take that SBOM we created with Syft and run it using Grype to see what vulnerabilities we have. (HINT: We should see the same things.) For our demonstration, you will not see any time savings but for larger code bases, the SBOM will save you time scanning.

```bash
docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock \
-v ${PWD}:/tmp --name grype anchore/grype:latest \
sbom:roman_decode_encode_sbom.json > roman_decode_encode_grype_sbom_report.txt
```

If you are running Docker in Windows then use the following command:

```bash
docker run --rm --volume "//var/run/docker.sock:/var/run/docker.sock" \
-v ${PWD}:/tmp --name grype anchore/grype:latest \
sbom:roman_decode_encode_sbom.json > roman_decode_encode_grype_sbom_report.txt
```
