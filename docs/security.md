# Security practices

- Keep the runtime dependency-free unless a dependency provides clear value.
- Store optional X API credentials in GitHub Actions secrets only.
- Use least-privilege workflow permissions.
- Treat fetched feed content and titles as untrusted input.
- Validate generated data before publishing it.
- Do not render fetched HTML as trusted markup.
- Review workflow changes carefully because scheduled jobs can write to the repository.
- Rotate credentials immediately if exposure is suspected.

URL-shape validation is not a guarantee that a destination is safe.