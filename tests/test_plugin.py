import pytest


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

    result.assert_outcomes(passed=10, failed=1)


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

    result.assert_outcomes(passed=10, failed=1)


# asdf_schema_skip_tests (with * with no ::foo, with ::foo)
# asdf_schema_xfail_tests (same as skip

# asdf_schema_skip_examples  (test schema but not examples?, nothing uses this)
# asdf_schema_validate_default (nothing uses this...)
# asdf_schema_ignore_unrecognized_tag (why is this a schema testing option?)


@pytest.mark.parametrize(
    "skip_cfg, expected",
    (
        ("schemas/valid-1.0.0", 10),
        ("schemas/nested/nested-1.0.0", 10),
        ("schemas/valid-1.0.0::*", 10),
        ("schemas/valid-1.0.0::0", 10),
        ("schemas/valid-1.0.0::2", 10),
    ),
)
def test_skips(pytester, skip_cfg, expected):
    pytester.copy_example("example")
    pytester.makepyprojecttoml(
        f"""
        [tool.pytest.ini_options]
        asdf_schema_root = 'resources/schemas'
        asdf_schema_tests_enabled = 'true'
        asdf_schema_ignore_unrecognized_tag = 'true'
        asdf_schema_skip_tests = '{skip_cfg}'
    """
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=expected, failed=1)
