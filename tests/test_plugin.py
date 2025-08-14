def test_example(pytester):
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

    result.assert_outcomes(passed=8)
