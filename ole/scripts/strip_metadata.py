def main():
    import argparse
    from pathlib import Path

    from specio.fileio import (
        MeasurementList_Notes,
        load_measurements,
        save_measurements,
    )

    from ole.utilities import get_valid_filename

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The csmf file to strip data from")

    parser.add_argument("-o", "--out-dir", help="Output directory", default=None)

    args = parser.parse_args()

    file_path = Path(args.file)
    file_data = load_measurements(str(file_path))

    output_path = file_path.parent if args.out_dir is None else Path(args.out_dir)

    file_data.metadata = MeasurementList_Notes(
        software="colour-workbench file stripper"
    )

    output_path = output_path.joinpath(
        get_valid_filename(file_data.shortname)
    ).with_suffix(".csmf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving anonymized data: {output_path!s} <- {file_path!s}")

    save_measurements(
        file=str(output_path),
        measurements=file_data.measurements.tolist(),
        order=file_data.order,
        testColors=file_data.test_colors,
        notes=MeasurementList_Notes(),
    )


if __name__ == "__main__":
    main()
