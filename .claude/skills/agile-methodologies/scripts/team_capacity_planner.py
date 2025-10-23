#!/usr/bin/env python3

import argparse
from typing import List, Dict

def calculate_capacity(
    team_members: List[str],
    sprint_days: int,
    daily_hours: float,
    leave_days: Dict[str, float],
    overhead_percentage: float,
    sp_conversion_factor: float = None,
    verbose: bool = False
) -> None:
    """
    Calculates and displays team capacity for a sprint.

    Args:
        team_members (List[str]): A list of team member names.
        sprint_days (int): The total number of working days in the sprint.
        daily_hours (float): Average daily working hours per team member.
        leave_days (Dict[str, float]): A dictionary mapping team member names to their planned leave days.
        overhead_percentage (float): Percentage of time reserved for overhead/unplanned work (e.g., 20 for 20%).
        sp_conversion_factor (float, optional): Conversion factor from hours to story points (e.g., 8 hours = 1 SP).
                                                If None, story points will not be calculated.
        verbose (bool): If True, print detailed processing messages.
    """
    if verbose:
        print("\n--- Team Capacity Planning ---")
        print(f"Sprint Duration: {sprint_days} days")
        print(f"Daily Availability: {daily_hours} hours/day")
        print(f"Overhead: {overhead_percentage}%")
        if sp_conversion_factor:
            print(f"Hours to Story Point Conversion: {sp_conversion_factor} hours/SP")
        print("------------------------------")

    total_available_hours = 0.0
    member_details = []

    for member in team_members:
        member_leave = leave_days.get(member, 0.0)
        member_working_days = sprint_days - member_leave
        member_working_hours = member_working_days * daily_hours
        total_available_hours += member_working_hours
        member_details.append({
            "name": member,
            "leave_days": member_leave,
            "working_days": member_working_days,
            "working_hours": member_working_hours
        })
        if verbose:
            print(f"{member}: {sprint_days} days - {member_leave} leave days = {member_working_days} working days ({member_working_hours:.2f} hours)")

    overhead_hours = total_available_hours * (overhead_percentage / 100.0)
    net_capacity_hours = total_available_hours - overhead_hours

    report = f"# Team Capacity Report\n\n"
    report += f"**Sprint Duration:** {sprint_days} working days\n"
    report += f"**Daily Working Hours per Person:** {daily_hours} hours\n"
    report += f"**Overhead/Buffer:** {overhead_percentage:.1f}%\n\n"

    report += "## Team Member Breakdown\n\n"
    report += "| Team Member | Planned Leave (Days) | Working Days | Available Hours |\n"
    report += "|-------------|----------------------|--------------|-----------------|"
    for member in member_details:
        report += f"\n| {member['name']} | {member['leave_days']:.1f} | {member['working_days']:.1f} | {member['working_hours']:.2f} |"
    report += "\n\n"

    report += "## Overall Team Capacity\n\n"
    report += f"- **Total Raw Available Hours:** {total_available_hours:.2f} hours\n"
    report += f"- **Hours Allocated for Overhead ({overhead_percentage:.1f}%):** {overhead_hours:.2f} hours\n"
    report += f"- **Net Capacity for Sprint Work:** **{net_capacity_hours:.2f} hours**\n"

    if sp_conversion_factor and sp_conversion_factor > 0:
        net_capacity_sp = net_capacity_hours / sp_conversion_factor
        report += f"- **Net Capacity in Story Points (assuming {sp_conversion_factor} hrs/SP):** **{net_capacity_sp:.2f} SP**\n"
    else:
        report += "\n*Story Point conversion not calculated (conversion factor not provided or invalid).*\n"

    print(report)

def main():
    parser = argparse.ArgumentParser(
        description='Calculate and display team capacity for a sprint.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--members', nargs='+', required=True,
                        help='List of team member names (e.g., "Alice Bob Charlie").')
    parser.add_argument('--sprint-days', type=int, default=10,
                        help='Total number of working days in the sprint (default: 10 for a 2-week sprint).')
    parser.add_argument('--daily-hours', type=float, default=8.0,
                        help='Average daily working hours per team member (default: 8.0).')
    parser.add_argument('--leave', nargs='*', default=[],
                        help='Planned leave days for team members (e.g., "Alice=1.5 Bob=2").')
    parser.add_argument('--overhead-percentage', type=float, default=20.0,
                        help='Percentage of time reserved for overhead/unplanned work (default: 20.0).')
    parser.add_argument('--sp-conversion', type=float,
                        help='Conversion factor from hours to story points (e.g., 8 for 8 hours = 1 SP).')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')

    args = parser.parse_args()

    leave_days_dict = {}
    for item in args.leave:
        if '=' in item:
            member, days_str = item.split('=', 1)
            try:
                leave_days_dict[member] = float(days_str)
            except ValueError:
                print(f"Warning: Invalid leave days format for '{item}'. Skipping.")
        else:
            print(f"Warning: Invalid leave format '{item}'. Expected 'Member=Days'. Skipping.")

    if args.sprint_days <= 0 or args.daily_hours <= 0 or args.overhead_percentage < 0:
        print("Error: Sprint days, daily hours must be positive, and overhead percentage non-negative.")
        return

    calculate_capacity(
        team_members=args.members,
        sprint_days=args.sprint_days,
        daily_hours=args.daily_hours,
        leave_days=leave_days_dict,
        overhead_percentage=args.overhead_percentage,
        sp_conversion_factor=args.sp_conversion,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()
