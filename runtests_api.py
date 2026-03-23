import sys
import pytest

pre_suite = []

parallel_suite = [
    "tests/api/test_api_agents.py",
    "tests/api/test_api_organization.py",
    "tests/api/test_api_role.py",
    "tests/api/test_api_user.py"
]

post_suite = []


def main():
    cli_args = sys.argv[1:]

    if pre_suite:
        print("\n[Phase 1] pre-suite...")
        exit_code = pytest.main(["-v", *cli_args, *pre_suite])
        if exit_code != 0:
            sys.exit(exit_code)

    print("\n[Phase 2] api tests...")
    exit_code = pytest.main(["-v", "--numprocesses=auto", "--dist=loadfile", *cli_args, *parallel_suite])
    if exit_code != 0:
        sys.exit(exit_code)

    if post_suite:
        print("\n[Phase 3] cleanup...")
        exit_code = pytest.main(["-v", *cli_args, *post_suite])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
