import os
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.models import (MODE_HOLD, MODE_PINNED, MediaType, Post, Status,  # noqa: E402
                          image_asset)
from igpub.schedule import assign_slots  # noqa: E402


def approved(pid, **kw):
    base = dict(id=pid, status=Status.APPROVED, media_type=MediaType.IMAGE, publish_at="",
                assets=[image_asset(f"{pid}.jpg")], approved_at="2026-06-01T00:00:00+00:00")
    base.update(kw)
    return Post(**base)


SCHED = {"timezone": "Asia/Tokyo", "slots": [{"time": "19:00"}],
         "rate": {"max_per_24h": 22, "min_gap_minutes": 180}, "horizon_days": 14, "blackout": []}
NOW = datetime(2026, 6, 25, 0, 0, tzinfo=timezone.utc)  # 09:00 JST on 2026-06-25


class TestJitter(unittest.TestCase):
    SCHED_J = {**SCHED, "jitter": {"min_minutes": -15, "max_minutes": 30}}

    def test_offset_within_window_and_deterministic(self):
        from datetime import datetime as _dt
        a = approved("jitterpost"); assign_slots([a], self.SCHED_J, NOW)
        b = approved("jitterpost"); assign_slots([b], self.SCHED_J, NOW)  # same id+day → same offset
        self.assertEqual(a.publish_at, b.publish_at)                       # deterministic across re-plans
        fire = _dt.fromisoformat(a.publish_at)
        self.assertEqual((fire.hour, fire.minute) >= (18, 45) or fire.hour == 19, True)
        mins = fire.hour * 60 + fire.minute
        self.assertTrue(18 * 60 + 45 <= mins <= 19 * 60 + 30)             # within [18:45, 19:30]

    def test_off_by_default_keeps_exact_slot(self):
        p = approved("nojit"); assign_slots([p], SCHED, NOW)               # SCHED has no jitter → off
        self.assertIn("T19:00:00", p.publish_at)


class TestWindow(unittest.TestCase):
    SCHED_W = {"timezone": "Asia/Tokyo", "slots": [{"window": ["08:00", "23:30"]}],
               "rate": {"max_per_24h": 22, "min_gap_minutes": 180}, "horizon_days": 14, "blackout": []}

    def test_time_inside_window_and_deterministic(self):
        from datetime import datetime as _dt
        a = approved("w1"); assign_slots([a], self.SCHED_W, NOW)
        b = approved("w1again"); assign_slots([b], self.SCHED_W, NOW)  # same first-free day → same seeded time
        self.assertEqual(a.publish_at[11:], b.publish_at[11:])
        t = _dt.fromisoformat(a.publish_at); mins = t.hour * 60 + t.minute
        self.assertTrue(8 * 60 <= mins <= 23 * 60 + 30)               # within [08:00, 23:30] JST
        self.assertFalse(a.publish_at.endswith("19:00:00+09:00") and "T19:00:00" in a.publish_at)  # not the old fixed slot

    def test_consecutive_posts_land_on_different_days(self):
        ps = [approved("d1"), approved("d2")]
        assign_slots(ps, self.SCHED_W, NOW)                           # min_gap pushes the 2nd to the next day
        self.assertNotEqual(ps[0].publish_at[:10], ps[1].publish_at[:10])


class TestAssignSlots(unittest.TestCase):
    def test_assigns_future_slot_and_marks_scheduled(self):
        p = approved("a")
        plan = assign_slots([p], SCHED, NOW)
        self.assertEqual(p.status, Status.SCHEDULED)
        self.assertIn("T19:00:00", p.publish_at)
        self.assertTrue(p.publish_at.endswith("+09:00"))
        self.assertEqual(len(plan.assignments), 1)

    def test_min_gap_spreads_to_separate_days(self):
        ps = [approved("a"), approved("b")]
        assign_slots(ps, SCHED, NOW)
        self.assertNotEqual(ps[0].publish_at, ps[1].publish_at)

    def test_priority_gets_earlier_slot(self):
        lo = approved("lo", priority=0)
        hi = approved("hi", priority=5)
        assign_slots([lo, hi], SCHED, NOW)
        self.assertLess(hi.publish_at, lo.publish_at)

    def test_hold_is_skipped(self):
        p = approved("h", schedule_mode=MODE_HOLD)
        plan = assign_slots([p], SCHED, NOW)
        self.assertEqual(p.status, Status.APPROVED)
        self.assertEqual(plan.assignments, [])
        self.assertEqual(plan.unscheduled, [])

    def test_pinned_reserved_and_blocks_collision(self):
        pin = approved("pin", schedule_mode=MODE_PINNED, publish_at="2026-06-25T19:00:00+09:00")
        auto = approved("auto")
        assign_slots([pin, auto], SCHED, NOW)
        self.assertEqual(pin.status, Status.SCHEDULED)
        self.assertNotEqual(auto.publish_at, "2026-06-25T19:00:00+09:00")

    def test_rerun_is_idempotent(self):
        p = approved("a")
        assign_slots([p], SCHED, NOW)
        first = p.publish_at
        plan2 = assign_slots([p], SCHED, NOW)   # p is now SCHEDULED → reserved, not reassigned
        self.assertEqual(p.publish_at, first)
        self.assertEqual(len(plan2.assignments), 1)

    def test_blackout_date_skipped(self):
        sched = dict(SCHED, blackout=["2026-06-25"])
        p = approved("a")
        assign_slots([p], sched, NOW)
        self.assertNotIn("2026-06-25", p.publish_at)

    def test_min_gap_pushes_second_to_next_day(self):
        # two slots 60min apart but min_gap=180 → the 2nd post can't take the same day's 2nd slot
        sched = {"timezone": "Asia/Tokyo", "slots": [{"time": "12:00"}, {"time": "13:00"}],
                 "rate": {"max_per_24h": 22, "min_gap_minutes": 180}, "horizon_days": 5, "blackout": []}
        ps = [approved("a"), approved("b")]
        assign_slots(ps, sched, NOW)
        self.assertTrue(ps[0].publish_at.startswith("2026-06-25"))
        self.assertTrue(ps[1].publish_at.startswith("2026-06-26"))   # pushed off the 60min-too-close slot

    def test_24h_cap_caps_per_window(self):
        # 3 slots today, cap=2/24h → only 2 fit, the rest go unscheduled (no free non-violating slot)
        sched = {"timezone": "Asia/Tokyo",
                 "slots": [{"time": "10:00"}, {"time": "12:00"}, {"time": "14:00"}],
                 "rate": {"max_per_24h": 2, "min_gap_minutes": 1}, "horizon_days": 0, "blackout": []}
        ps = [approved(f"p{i}") for i in range(4)]
        plan = assign_slots(ps, sched, NOW)
        self.assertEqual(len(plan.assignments), 2)
        self.assertEqual(len(plan.unscheduled), 2)


if __name__ == "__main__":
    unittest.main()
