import warnings

# Passlib still imports the deprecated stdlib `crypt` module when available.
# Filter the warning globally so it doesn't pollute the test output.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"passlib\.utils.*",
)
