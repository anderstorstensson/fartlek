"""Process-wide test isolation. MUST stay in conftest.py.

backend.config freezes its AppConfig singleton at first import, so these
environment variables must be set before ANY test module imports backend
code. pytest loads conftest.py before collecting test modules, which makes
this the only place that guarantees the ordering — setting the variables at
the top of an individual test file only works if that file happens to be
imported first. (Learned the hard way: running `pytest tests/test_gcal.py
tests/test_api.py` once pointed the API tests at the real database.)
"""

import os
import tempfile

import pytest

os.environ["FARTLEK_SCHEDULER_ENABLED"] = "0"
os.environ["FARTLEK_DATA_DIR"] = tempfile.mkdtemp(prefix="fartlek-test-")


@pytest.fixture(scope="session", autouse=True)
def _refuse_to_run_against_real_data():
    """Hard stop if the config singleton froze on a non-test data dir (e.g.
    because something imported backend before this conftest ran)."""
    from backend.config import config

    if str(config.data_dir) != os.environ["FARTLEK_DATA_DIR"]:
        pytest.exit(
            f"Test isolation failure: backend.config points at {config.data_dir}, "
            "not the test temp dir. Refusing to run against real data.",
            returncode=3,
        )
