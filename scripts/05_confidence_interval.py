from common import (
    get_test_variables,
    mean_confidence_interval,
    OUTPUT_FOLDER
)


output_file = (
    OUTPUT_FOLDER /
    "05_confidence_interval_output.txt"
)


sample, progressed, eliminated = (
    get_test_variables()
)


progressed_ci = (
    mean_confidence_interval(
        progressed
    )
)


eliminated_ci = (
    mean_confidence_interval(
        eliminated
    )
)


output = f"""
{'=' * 80}
5. INFERENTIAL STATISTICS - 95% CONFIDENCE INTERVAL
{'=' * 80}

PROGRESSED-TEAM FORWARDS

Sample size:
n = {progressed_ci['n']}

Mean SoT/90:
{progressed_ci['mean']:.3f}

Standard deviation:
{progressed_ci['standard_deviation']:.3f}

Standard error:
{progressed_ci['standard_error']:.3f}

95% Confidence Interval:
[{progressed_ci['lower']:.3f}, {progressed_ci['upper']:.3f}]


ELIMINATED-TEAM FORWARDS

Sample size:
n = {eliminated_ci['n']}

Mean SoT/90:
{eliminated_ci['mean']:.3f}

Standard deviation:
{eliminated_ci['standard_deviation']:.3f}

Standard error:
{eliminated_ci['standard_error']:.3f}

95% Confidence Interval:
[{eliminated_ci['lower']:.3f}, {eliminated_ci['upper']:.3f}]
"""


output_file.write_text(
    output,
    encoding="utf-8"
)


print(output)

print(
    "\nOutput automatically saved to:"
)

print(output_file)