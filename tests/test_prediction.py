from datetime import datetime, timedelta

from backend.analysis.prediction import riegel_time


def test_riegel_10k_from_5k():
    # 20:00 5K → ~41:30 10K with exponent 1.06
    predicted = riegel_time(5000, 1200, 10000)
    assert 2480 < predicted < 2510


def test_riegel_same_distance_is_identity():
    assert riegel_time(10000, 2400, 10000) == 2400


def test_marathon_prediction_ignores_short_anchors(tmp_path):
    """Only anchors ≥ 1/5 of goal distance qualify; the fastest wins."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from backend.analysis.prediction import predict
    from backend.db import Base
    from backend.models import BestEffort

    engine = create_engine(f"sqlite:///{tmp_path}/pred.sqlite3")
    Base.metadata.create_all(engine)
    now = datetime.now()
    with Session(engine) as session:
        session.add_all([
            # absurd 1K (spike leftovers) must not vote on a marathon
            BestEffort(activity_id=1, label="1K", distance_m=1000, duration_s=150,
                       start_time_utc=now - timedelta(days=5)),
            BestEffort(activity_id=1, label="10K", distance_m=10000, duration_s=2342,
                       start_time_utc=now - timedelta(days=5)),
            BestEffort(activity_id=2, label="Half marathon", distance_m=21097.5,
                       duration_s=4988, start_time_utc=now - timedelta(days=18)),
        ])
        session.commit()

        marathon = predict(session, 42195)
        # half 1:23:08 → ~2:53; 10K 39:02 → ~3:00; 1K excluded despite being "fastest"
        assert marathon.anchor_label == "Half marathon"
        assert 10350 < marathon.time_s < 10450

        # for a 5K goal the 1K qualifies again
        five_k = predict(session, 5000)
        assert five_k.anchor_label == "1K"
