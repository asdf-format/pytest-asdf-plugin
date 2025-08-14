import pytest

# the example schemas have a number of successes and failures
# hard-code them here to allow more flexibility in the tests below
PASSES = 9
FAILURES = 3


def test_pyprojecttoml(pytester):
    pytester.copy_example("example")
    pytester.makepyprojecttoml(
        """
        [tool.pytest.ini_options]
        asdf_schema_root = 'resources/schemas'
        asdf_schema_tests_enabled = 'true'
        asdf_schema_ignore_unrecognized_tag = 'true'
    """
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=PASSES, failed=FAILURES)


def test_asdf_tests_argument(pytester):
    pytester.copy_example("example")
    pytester.makepyprojecttoml(
        """
        [tool.pytest.ini_options]
        asdf_schema_root = 'resources/schemas'
        asdf_schema_ignore_unrecognized_tag = 'true'
    """
    )
    result = pytester.runpytest("--asdf-tests")

    result.assert_outcomes(passed=PASSES, failed=FAILURES)


# asdf_schema_skip_tests (with * with no ::foo, with ::foo)
# asdf_schema_xfail_tests (same as skip

# asdf_schema_skip_examples  (test schema but not examples?, nothing uses this)
# asdf_schema_validate_default (nothing uses this...)
# asdf_schema_ignore_unrecognized_tag (why is this a schema testing option?)


@pytest.mark.parametrize(
    "skip_cfg, passes, failures, skips",
    (
        ("passing-1.0.0.yaml", PASSES - 4, FAILURES, 4),
        ("passing-1.0.0.yaml::*", PASSES - 4, FAILURES, 4),
        ("passing-1.0.0.yaml::test_example_0", PASSES - 1, FAILURES, 1),
        ("passing-1.0.0.yaml::test_example_1", PASSES - 1, FAILURES, 1),
        ("nested/nested-1.0.0.yaml", PASSES - 4, FAILURES, 4),
    ),
)
def test_skips(pytester, skip_cfg, passes, failures, skips):
    pytester.copy_example("example")
    pytester.makepyprojecttoml(
        f"""
        [tool.pytest.ini_options]
        asdf_schema_root = 'resources/schemas'
        asdf_schema_tests_enabled = 'true'
        asdf_schema_ignore_unrecognized_tag = 'true'
        asdf_schema_skip_tests = "{skip_cfg}"
    """
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=passes, failed=failures, skipped=skips)
