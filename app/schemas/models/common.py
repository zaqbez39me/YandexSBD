import re
from datetime import time

from pydantic import BaseModel, validator
from pydantic.types import conint, constr

int32 = conint(strict=False, ge=-(2**31), le=2**31 - 1)
int64 = conint(strict=False, ge=-(2**63), le=2**63 - 1)


class Hours(BaseModel):
    hours: constr(
        regex="(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1]["
        "0-9])|(2[0-3])):[0-5][0-9]"
    )

    @validator("hours")
    def validate_hours(cls, hours):
        start_hour, start_minute, finish_hour, finish_minute = map(
            int, re.split("[:-]", hours)
        )
        start_time = time(hour=start_hour, minute=start_minute)
        finish_time = time(hour=finish_hour, minute=finish_minute)
        if finish_time < start_time:
            raise ValueError(hours)
        return hours

    @property
    def start_time(self):
        start_hour, start_minute, _, _ = map(int, re.split("[:-]", self.hours))
        return time(hour=start_hour, minute=start_minute)

    @property
    def end_time(self):
        _, _, end_hour, end_minute = map(int, re.split("[:-]", self.hours))
        return time(hour=end_hour, minute=end_minute)

    def do_intersect(self, other: "Hours"):
        other_start, other_end = other.start_time, other.end_time
        self_start, self_end = self.start_time, self.end_time
        return (
            other_start < self_end < other_end
            or self_start < other_start < self_end
        )


class HoursList(list[Hours]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, list):
            raise ValueError("List of hours strings required")
        return cls.working_hours_validator(v)

    @classmethod
    def working_hours_validator(cls, hours):
        errors = {}
        hours_instances = []
        for hour in hours:
            try:
                hours_instances.append(Hours(hours=hour))
            except ValueError as value_error:
                if "time_diff_error" not in errors:
                    errors["time_diff_error"] = []
                errors["time_diff_error"].append(str(value_error))
        hours_instances.sort(key=lambda x: x.start_time)
        if not errors:
            for i in range(len(hours_instances) - 1):
                if hours_instances[i].do_intersect(hours_instances[i + 1]):
                    if "time_intersect_error" not in errors:
                        errors["time_intersect_error"] = []
                    errors["time_intersect_error"].append(
                        f"{hours[i]} intersects with {hours[i + 1]}"
                    )
        if errors:
            raise ValueError(errors)
        return hours
