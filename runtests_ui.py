import sys
import pytest

pre_suite = [
    "tests/ui/test_smoke.py",
]

parallel_suite = [
    "tests/ui/test_login.py",
    "tests/ui/test_organization.py"
]

post_suite = [
    "tests/ui/test_get_data_ids_delete.py"
]


def main():
    cli_args = sys.argv[1:]

    print("\n[Phase 1] smoke...")
    exit_code = pytest.main(["-v", *cli_args, *pre_suite])
    if exit_code != 0:
        sys.exit(exit_code)

    print("\n[Phase 2] ui tests...")
    exit_code = pytest.main(["-v", "--numprocesses=auto", "--dist=loadfile", *cli_args, *parallel_suite])
    if exit_code != 0:
        sys.exit(exit_code)

    if post_suite:
        print("\n[Phase 3] cleanup...")
        exit_code = pytest.main(["-v", *cli_args, *post_suite])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
