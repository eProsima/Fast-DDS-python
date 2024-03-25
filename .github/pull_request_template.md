<!-- Provide a general summary of your changes in the Title above -->
<!-- It must be meaningful and coherent with the changes -->

<!--
    If this PR is still a Work in Progress [WIP], please open it as DRAFT.
    Please consider if any label should be added to this PR.
-->

## Description
<!--
    Describe changes in detail.
    This includes depicting the context, use case or current behavior and describe the proposed changes.
    If several features/bug fixes are included with these changes, please consider opening separated pull requests.
-->

<!--
    In case of bug fixes, please provide the list of supported branches where this fix should be also merged.
    Please uncomment following line, adjusting the corresponding target branches for the backport.
-->
<!-- @Mergifyio backport 1.4.x 1.2.x 1.0.x -->

<!-- If an issue is already opened, please uncomment next line with the corresponding issue number. -->
<!-- Fixes #(issue) -->

<!-- In case the changes are built over a previous pull request, please uncomment next line. -->
<!-- This PR depends on #(PR) and must be merged after that one. -->

## Contributor Checklist

- [ ] Commit messages follow the project guidelines. <!-- External contributors should sign the DCO. Fast DDS Python developers must also refer to the internal Redmine task. -->
- [ ] Tests that thoroughly check the new feature have been added/Regression tests checking the bug and its fix have been added; the added tests pass locally
- [ ] Changes are API compatible. <!-- Public API must not be broken within the same major release. -->
- [ ] Applicable backports have been included in the description.

## Reviewer Checklist

- [ ] The PR has a milestone assigned.
- [ ] The title and description correctly express the PR's purpose.
- [ ] Check contributor checklist is correct.
- [ ] Check CI results: changes do not issue any warning.
- [ ] Check CI results: failing tests are unrelated with the changes.
