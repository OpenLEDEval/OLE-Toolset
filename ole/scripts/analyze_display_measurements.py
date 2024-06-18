"""
Script module for analyzing display measurement files and generating PDFs.
"""

from colour.utilities.verbose import suppress_warnings
from specio import get_valid_filename
from specio.serialization.csmf import CSMF_Metadata


def main():
    """
    The entry point for measurement analysis and PDF generation.
    """  # noqa: D401
    import argparse
    from pathlib import Path

    from matplotlib import pyplot as plt

    from ole.ETC import (
        analyze_measurements_from_file,
        generate_report_page,
    )
    from ole.ETC.analysis import ReflectanceData

    program_description = """
    Create the ETC LED Evaluation Report for a particular measurement file.
    """
    parser = argparse.ArgumentParser(
        prog="ETC Display Measurements", description=program_description
    )

    parser.add_argument("file", help="The input file.")

    parser.add_argument(
        "-o",
        "--out",
        help=(
            "The output file name. If the output is not a file name with the "
            "extension .pdf, a directory will be created and the file name "
            "will be determined by the contents of the measurement file name "
            "will be determined by the contents of the measurements."
        ),
        default=None,
    )

    parser.add_argument(
        "--rf_45_0",
        help="45:0 reflectance factor (not as percentage)",
        default=None,
    )

    parser.add_argument(
        "--rf_45_45",
        help="45:-45 reflectance factor (not as percentage)",
        default=None,
    )

    parser.add_argument(
        "--strip-details",
        action="store_true",
        help="Remove metadata / notes from the output PDF",
    )

    args = parser.parse_args()

    # Check File
    in_file = Path(args.file)
    if not in_file.exists() or not in_file.is_file():
        raise FileNotFoundError()

    # Analyze data
    data = analyze_measurements_from_file(str(in_file))

    if args.strip_details:
        data.metadata = CSMF_Metadata(software=None)
        data.shortname = f"ETC Display Analysis - {data.shortname}"

    reflectance = (
        ReflectanceData(reflectance_45_0=args.rf_45_0, reflectance_45_45=args.rf_45_45)
        if (args.rf_45_0 is not None and args.rf_45_45 is not None)
        else None
    )

    # Determine output file name
    if args.out:
        out_file_name = Path(args.out)
        if out_file_name.suffix == ".pdf":
            out_file_name.parent.mkdir(parents=True, exist_ok=True)
        elif out_file_name.suffix != "":
            raise RuntimeError("File name must end in .pdf")
        else:
            out_file_name.mkdir(parents=True, exist_ok=True)
            out_file_name = out_file_name.joinpath(get_valid_filename(data.shortname))
    else:
        out_file_name = in_file.with_suffix(".pdf")

    out_file_name = out_file_name.with_suffix(".pdf")

    # Generate PDF

    fig = generate_report_page(color_data=data, reflectance_data=reflectance)

    fig.savefig(str(out_file_name), facecolor=[1, 1, 1])

    print(f"Analysis saved to: {out_file_name!s}")  # noqa: T201
    plt.close(fig)


if __name__ == "__main__":
    print("Ignoring colour warnings")  # noqa: T201
    with suppress_warnings(colour_warnings=True, python_warnings=True):
        main()
