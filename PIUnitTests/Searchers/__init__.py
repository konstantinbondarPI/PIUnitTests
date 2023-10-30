from dataclasses import dataclass, field


@dataclass(frozen=True)
class SearchConfig:
    search_directories: list[str] = field(default_factory=list)
    filename_rules: list[str] = field(default_factory=list)
    function_rules: list[str] = field(default_factory=list)
    in_depth_search: bool = True
    only_matched_files_check: bool = False

