# Publication provenance

Public distribution uses a reviewed source snapshot with a fresh root commit. Earlier development history, source originals, verification logs and previous private releases are preserved separately and remain private. They are not merged or mirrored into the public source repository.

The owner approved this separation so earlier artwork copies and private development records do not become public merely because the current files were repaired. Component licenses and required notices stay with the current source; a fresh history does not replace that requirement.

## Publication gates

1. Preserve and verify a private recovery copy before changing repository identity.
2. Build the replacement repository privately from an explicit reviewed file inventory. Copy no old Git objects, private originals, generated workspaces or local review logs.
3. Independently review the exact tree and commit metadata, including source and provenance links, examples, configuration, image frames/metadata and release archive members. Investigate suspicious hits; scanner silence is not proof of privacy.
4. Verify all reachable objects of the new repository, exact source identity, reproducible packaging and Linux CI against its saved root commit.
5. Complete the final independent readback before changing visibility. Verify the private archive remains private and confirm the public repository's exact commit and CI afterward.

These gates describe the release procedure. The version-bound release handover records which actions and checks actually completed. No original archive, local review transcript or earlier CI log belongs in the public distribution.

## Future changes

Review new files and full reachable history before each push. An approved image digest covers only those exact bytes at its declared path; changed or additional binary content requires a new complete content review. Keep company work outside reusable source. Do not infer a blanket reuse license, installation authority, company permission or business outcome from publication.
