#!/usr/bin/env python
"""
Example calculation script that creates multiple result files.
Replace this with your actual calculation script.
"""
import argparse
import time
import random
import os
import json


def parse_args():
    parser = argparse.ArgumentParser(description='Calculation script')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for results')
    parser.add_argument('--job_id', type=int, required=True, help='Job ID')
    parser.add_argument('--iterations', type=int, default=5, help='Number of iterations')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between iterations')

    # Add any other parameters your calculation needs
    parser.add_argument('--param1', type=float, default=1.0, help='Parameter 1')
    parser.add_argument('--param2', type=float, default=2.0, help='Parameter 2')

    return parser.parse_args()


def run_calculation(args):
    print(f"Starting calculation job {args.job_id}")
    print(f"Parameters: iterations={args.iterations}, param1={args.param1}, param2={args.param2}")

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Run the calculation for the specified number of iterations
    for i in range(args.iterations):
        print(f"Running iteration {i + 1}/{args.iterations}")

        # Simulate your calculation here
        time.sleep(args.delay)

        # Generate some random data
        data = {
            'iteration': i + 1,
            'param1': args.param1,
            'param2': args.param2,
            'result': args.param1 * args.param2 * random.random()
        }

        # Save the result to a file
        filename = f"job_{args.job_id}_iteration_{i + 1}.raw"
        filepath = os.path.join(args.output_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Saved result to {filepath}")

    print(f"Calculation job {args.job_id} completed")
    return 0


if __name__ == '__main__':
    args = parse_args()
    exit_code = run_calculation(args)
    exit(exit_code)