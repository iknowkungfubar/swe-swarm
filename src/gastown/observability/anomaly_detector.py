"""
Anomaly detector for Gastown Swarm.
"""

import time
from collections import deque
from typing import Any

from loguru import logger


class AnomalyDetector:
    """Detects anomalies in metrics and triggers alerts."""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.history: dict[str, deque[float]] = {}
        self.thresholds: dict[str, dict[str, float]] = {}
        self.alerts: list[dict[str, Any]] = []

        # Default thresholds
        self.set_threshold("error_rate", warning=0.1, critical=0.3)
        self.set_threshold("iteration_duration", warning=10.0, critical=30.0)
        self.set_threshold("task_failure_rate", warning=0.05, critical=0.2)

    def set_threshold(self, metric_name: str, warning: float, critical: float):
        """Set alert thresholds for a metric."""
        self.thresholds[metric_name] = {
            "warning": warning,
            "critical": critical,
        }
        if metric_name not in self.history:
            self.history[metric_name] = deque(maxlen=self.window_size)

    def record_metric(self, metric_name: str, value: float):
        """Record a metric value and check for anomalies."""
        if metric_name not in self.history:
            self.history[metric_name] = deque(maxlen=self.window_size)

        self.history[metric_name].append(value)

        # Check thresholds if defined
        if metric_name in self.thresholds:
            self._check_thresholds(metric_name, value)

    def _check_thresholds(self, metric_name: str, value: float):
        """Check if value exceeds thresholds."""
        thresholds = self.thresholds[metric_name]

        if value >= thresholds["critical"]:
            alert = {
                "timestamp": time.time(),
                "metric": metric_name,
                "value": value,
                "severity": "critical",
                "threshold": thresholds["critical"],
                "message": (
                    f"{metric_name} = {value} exceeds critical threshold "
                    f"{thresholds['critical']}"
                ),
            }
            self.alerts.append(alert)
            logger.critical(alert["message"])

        elif value >= thresholds["warning"]:
            alert = {
                "timestamp": time.time(),
                "metric": metric_name,
                "value": value,
                "severity": "warning",
                "threshold": thresholds["warning"],
                "message": (
                    f"{metric_name} = {value} exceeds warning threshold "
                    f"{thresholds['warning']}"
                ),
            }
            self.alerts.append(alert)
            logger.warning(alert["message"])

    def check_trend(
        self, metric_name: str, lookback: int = 10
    ) -> dict[str, Any] | None:
        """
        Check for trending anomalies (increasing/decreasing trend).

        Returns trend analysis if significant.
        """
        if metric_name not in self.history:
            return None

        history = list(self.history[metric_name])
        if len(history) < lookback:
            return None

        recent = history[-lookback:]
        avg_recent = sum(recent) / len(recent)
        avg_historical = sum(history[:-lookback]) / max(1, len(history) - lookback)

        if avg_historical == 0:
            return None

        change_pct = (avg_recent - avg_historical) / avg_historical * 100

        if abs(change_pct) > 50:  # Significant change
            trend = "increasing" if change_pct > 0 else "decreasing"
            return {
                "metric": metric_name,
                "trend": trend,
                "change_percent": change_pct,
                "recent_avg": avg_recent,
                "historical_avg": avg_historical,
                "message": f"{metric_name} is {trend} by {change_pct:.1f}%",
            }
        return None

    def get_recent_alerts(self, count: int = 10) -> list[dict[str, Any]]:
        """Get recent alerts."""
        return self.alerts[-count:]

    def clear_alerts(self):
        """Clear all alerts."""
        self.alerts.clear()
        logger.info("Alerts cleared")

    def get_metric_stats(self, metric_name: str) -> dict[str, Any] | None:
        """Get statistics for a metric."""
        if metric_name not in self.history:
            return None

        values = list(self.history[metric_name])
        if not values:
            return None

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1],
        }

    def detect_anomalies(self) -> list[dict[str, Any]]:
        """Run detection on all metrics and return anomalies."""
        anomalies = []

        for metric_name in self.history:
            trend = self.check_trend(metric_name)
            if trend:
                anomalies.append(trend)

        return anomalies

    def get_status(self) -> dict[str, Any]:
        """Get detector status."""
        return {
            "window_size": self.window_size,
            "metrics_tracked": len(self.history),
            "alerts_total": len(self.alerts),
            "thresholds": self.thresholds,
        }
