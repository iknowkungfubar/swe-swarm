"""
Metrics collector for Gastown Swarm.
"""

import time
from collections import defaultdict
from typing import Any

from loguru import logger


class MetricsCollector:
    """Collects and aggregates metrics from the swarm."""

    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.timers: dict[str, list[float]] = defaultdict(list)
        self.gauges: dict[str, float] = defaultdict(float)
        self.histograms: dict[str, list[float]] = defaultdict(list)
        self.start_time = time.time()

    def increment(self, name: str, value: int = 1):
        """Increment a counter."""
        self.counters[name] += value
        logger.debug(f"Metric increment {name}: {value}")

    def decrement(self, name: str, value: int = 1):
        """Decrement a counter."""
        self.counters[name] -= value
        logger.debug(f"Metric decrement {name}: {value}")

    def set_gauge(self, name: str, value: float):
        """Set a gauge value."""
        self.gauges[name] = value
        logger.debug(f"Gauge set {name}: {value}")

    def start_timer(self, name: str) -> str:
        """Start a timer and return a timer ID."""
        timer_id = f"{name}_{int(time.time() * 1000)}"
        self.timers[timer_id] = [time.time()]
        return timer_id

    def stop_timer(self, timer_id: str) -> float:
        """Stop a timer and return elapsed time in seconds."""
        if timer_id not in self.timers:
            logger.warning(f"Timer {timer_id} not found")
            return 0.0
        start = self.timers[timer_id][0]
        elapsed = time.time() - start
        self.timers[timer_id].append(elapsed)
        # Store in histogram under original name
        name = timer_id.rsplit("_", 1)[0]
        self.histograms[name].append(elapsed)
        logger.debug(f"Timer {name} elapsed: {elapsed:.3f}s")
        return elapsed

    def record_histogram(self, name: str, value: float):
        """Record a value in a histogram."""
        self.histograms[name].append(value)
        logger.debug(f"Histogram {name}: {value}")

    def get_counter(self, name: str) -> int:
        """Get current counter value."""
        return self.counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        """Get current gauge value."""
        return self.gauges.get(name, 0.0)

    def get_histogram_stats(self, name: str) -> dict[str, Any]:
        """Get statistics for a histogram."""
        values = self.histograms.get(name, [])
        if not values:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "sum": 0}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "sum": sum(values),
        }

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all collected metrics."""
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histories": {
                name: self.get_histogram_stats(name) for name in self.histograms
            },
        }

    def reset(self):
        """Reset all metrics."""
        self.counters.clear()
        self.timers.clear()
        self.gauges.clear()
        self.histograms.clear()
        self.start_time = time.time()
        logger.info("Metrics reset")

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format (simple)."""
        lines = []
        lines.append("# HELP gastown_uptime_seconds Total uptime in seconds")
        lines.append("# TYPE gastown_uptime_seconds gauge")
        lines.append(f"gastown_uptime_seconds {time.time() - self.start_time}")

        for name, value in self.counters.items():
            lines.append(f"# HELP gastown_{name} Counter")
            lines.append(f"# TYPE gastown_{name} counter")
            lines.append(f"gastown_{name} {value}")

        for name, value in self.gauges.items():
            lines.append(f"# HELP gastown_{name} Gauge")
            lines.append(f"# TYPE gastown_{name} gauge")
            lines.append(f"gastown_{name} {value}")

        return "\n".join(lines)
