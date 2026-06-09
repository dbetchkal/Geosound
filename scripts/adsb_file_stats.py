from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, median
from tabnanny import verbose


@dataclass
class YearStats:
    files: int = 0
    files_bytes: int = 0
    dates: set[str] = field(default_factory=set)
    dirs: Counter[str] = field(default_factory=Counter)
    sizes_mb: list[float] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize ADS-B TSV collections."
    )

    parser.add_argument(
        "root",
        type=Path,
        help="Root directory containing '<YEAR> ADS-B <SITE>' folders.",
    )

    parser.add_argument(
        "-e",
        "--extension",
        default=r".tsv",
        help="File extension to look for (default: .tsv).",
    )

    return parser.parse_args()


def collect_stats(root: Path, file_extension: str) -> dict[str, dict[str, YearStats]]:
    stats: dict[str, dict[str, YearStats]] = defaultdict(
        lambda: defaultdict(YearStats)
    )

    for site_dir in root.iterdir():
        if not site_dir.is_dir():
            continue

        parts = site_dir.name.split(" ADS-B ", maxsplit=1)
        if len(parts) != 2:
            continue

        year, site = parts

        for tsv in site_dir.rglob(pattern=fr"*{file_extension}", case_sensitive=False):
            s = stats[site][year]

            size_bytes = tsv.stat().st_size

            s.files += 1
            s.files_bytes += size_bytes
            s.dates.add(tsv.name.upper())
            s.dirs[tsv.parent.name] += 1
            s.sizes_mb.append(size_bytes / 1024**2)

    if not stats:
        print(f"No files with extension '{file_extension}' found in a recursive search starting at '{root}'" 
              "and searching for site dirs with pattern '<YEAR> ADS-B <SITE>'.")
        exit(1)

    return stats


def print_site(site: str, yearly_stats: dict[str, YearStats]) -> None:
    print(f"\n{site}")
    print("=" * len(site))

    total_files = 0
    total_bytes = 0
    total_dates: set[str] = set()

    for year in sorted(yearly_stats):
        s = yearly_stats[year]

        total_files += s.files
        total_bytes += s.files_bytes
        total_dates.update(s.dates)

        dup = s.files / len(s.dates) if s.dates else float("nan")

        print(
            f"{year} | "
            f"{len(s.dates):>3} dates | "
            f"{s.files:>3} files | "
            f"{s.files_bytes / 1024**3:>5.2f} GB | "
            f"dup={dup:.2f}x"
        )

        for dirname, count in s.dirs.most_common():
            print(f"    {dirname:<20} {count:>4} files")

            print(
                f"    size stats: "
                f"mean={mean(s.sizes_mb):.1f} MB, "
                f"median={median(s.sizes_mb):.1f} MB, "
                f"min={min(s.sizes_mb):.1f} MB, "
                f"max={max(s.sizes_mb):.1f} MB"
            )

    print(
        f"\nTOTAL | "
        f"{len(total_dates):>3} dates | "
        f"{total_files:>3} files | "
        f"{total_bytes / 1024**3:>5.2f} GB"
    )


def main() -> None:
    args = parse_args()
    
    stats = collect_stats(args.root, args.extension)

    for site in sorted(stats):
        print_site(site, stats[site])


if __name__ == "__main__":
    main()