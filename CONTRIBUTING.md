# Contributing to SyncSound

We love your input! We want to make contributing to SyncSound as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests

1.  **Fork the repo** and create your branch from `master`.
2.  If you've added code that should be tested, add tests.
3.  If you've changed APIs, update the documentation.
4.  Ensure the test suite passes.
5.  Make sure your code lints.
6.  Issue that pull request!

## Local Development Workflow

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/aaditx/SyncMusic.git
    cd SyncMusic
    ```

2.  **Create a Feature Branch**:
    ```bash
    git checkout -b feature/my-amazing-feature
    ```

3.  **Make Changes**: Edit files in `backend/` or `backend/app/static/`.

4.  **Test Locally**:
    ```bash
    # Run backend tests
    cd backend
    pytest
    ```

5.  **Commit and Push**:
    ```bash
    git add .
    git commit -m "feat: add amazing feature"
    git push origin feature/my-amazing-feature
    ```

6.  **Open a Pull Request** on GitHub.

## Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Commits**: Use descriptive commit messages (e.g., `feat: ...`, `fix: ...`, `docs: ...`).

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
