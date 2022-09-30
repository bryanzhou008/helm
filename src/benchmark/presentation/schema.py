from dataclasses import dataclass, field
from typing import List, Optional, Dict
import dacite
import mako.template
import yaml

from common.general import hlog
from benchmark.metrics.metric_name import MetricName
from benchmark.augmentations.perturbation_description import PERTURBATION_WORST

SCHEMA_YAML_PATH: str = "src/proxy/static/schema.yaml"
UP_ARROW = "\u2191"
DOWN_ARROW = "\u2193"


@dataclass(frozen=True)
class Field:
    """
    Represents a field in a specification (e.g., `temperature` for the adapter,
    or `exact_match` for metrics or `typos` for perturbations.
    """

    # Internal name (usually no spaces, etc.)
    name: str

    # What is displayed to the user
    display_name: Optional[str] = None

    # What is displayed to the user (e.g., in a table header)
    short_display_name: Optional[str] = None

    # Description of the field
    description: Optional[str] = None

    # Whether a lower vaue for this field corresponds to a better model (e.g., False for accuracy, True for perplexity)
    lower_is_better: bool = False

    def get_short_display_name(self, arrow: bool = False) -> str:
        name = self.short_display_name or self.display_name or self.name
        if arrow:
            name += " " + (DOWN_ARROW if self.lower_is_better else UP_ARROW)
        return name


@dataclass(frozen=True)
class MetricNameMatcher:
    """
    The schema file specifies information about what metrics we want to specify,
    but it doesn't specify full `MetricName`s.  Instead, it specifies enough
    information in a `MetricNameMatcher` to pull out the relevant
    `MetricName`s.
    """

    # Name of the metric
    name: str

    # Which data split to report numbers on (e.g., TEST_SPLIT)
    split: str

    # Which sub split to report numbers on (e.g., toxic, non-toxic)
    sub_split: Optional[str] = None

    # Which perturbation to show (e.g., robustness)
    perturbation_name: Optional[str] = None

    def matches(self, metric_name: MetricName) -> bool:
        if self.name != metric_name.name or self.split != metric_name.split or self.sub_split != metric_name.sub_split:
            return False

        metric_perturbation_name = metric_name.perturbation and metric_name.perturbation.name
        if self.perturbation_name != metric_perturbation_name:
            return False

        # If there is a perturbation, only return the worst
        if metric_name.perturbation and metric_name.perturbation.computed_on != PERTURBATION_WORST:
            return False
        return True

    def substitute(self, environment: Dict[str, str]) -> "MetricNameMatcher":
        return MetricNameMatcher(
            name=mako.template.Template(self.name).render(**environment),
            split=mako.template.Template(self.split).render(**environment),
            perturbation_name=mako.template.Template(self.perturbation_name).render(**environment)
            if self.perturbation_name is not None
            else None,
        )


@dataclass(frozen=True)
class MetricGroup(Field):
    """
    A list of metrics (which are presumably logically grouped).
    """

    metrics: List[MetricNameMatcher] = field(default_factory=list)


BY_METRIC = "by_metric"
BY_GROUP = "by_group"


@dataclass(frozen=True)
class RunGroup(Field):
    """
    Defines information about how a group of runs is displayed.
    """

    # What groups (by name) to show
    metric_groups: List[str] = field(default_factory=list)

    # Names of subgroups which this group contains. That is, when displaying this group, we will also (recursively)
    # display all of its subgroups. This allows us to aggregate runs in different ways without having to explicitly
    # annotate each run. For instance, we can display MMLU with the group "QA" by adding it as a subgroup.
    subgroups: List[str] = field(default_factory=list)

    # When displaying the subgroups, should each table show all the metrics for each group (BY_GROUP) or show all the
    # groups for each metric (BY_METRIC)
    subgroup_display_mode: str = BY_METRIC

    # Defines variables that are substituted in any of the metrics
    environment: Dict[str, str] = field(default_factory=dict)

    # Which category this group belongs to. These currently include "Scenarios", "Tasks", "Components" and are used to
    # clump different groups together for easier website navigation.
    category: str = "Scenarios"


@dataclass
class Schema:
    """Specifies information about what to display on the frontend."""

    # Adapter fields (e.g., temperature)
    adapter: List[Field]

    # Information about each field
    metrics: List[Field]

    # Information about each perturbation
    perturbations: List[Field]

    # Group the metrics
    metric_groups: List[MetricGroup]

    # Group the scenarios
    run_groups: List[RunGroup]

    def __post_init__(self):
        self.name_to_metric = {metric.name: metric for metric in self.metrics}
        self.name_to_perturbation = {perturbation.name: perturbation for perturbation in self.perturbations}
        self.name_to_metric_group = {metric_group.name: metric_group for metric_group in self.metric_groups}
        self.name_to_run_group = {run_group.name: run_group for run_group in self.run_groups}


def read_schema():
    hlog(f"Reading schema from {SCHEMA_YAML_PATH}...")
    with open(SCHEMA_YAML_PATH) as f:
        raw = yaml.safe_load(f)
    return dacite.from_dict(Schema, raw)