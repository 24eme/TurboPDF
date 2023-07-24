from PyPDF2 import PdfReader, PdfWriter
import argparse
import os.path
import shutil
import subprocess
import sys
import os 

def compress(input_file_path, output_file_path, power=0):
    """Function to compress PDF via Ghostscript command line interface"""
    quality = {0: "/default", 1: "/prepress", 2: "/printer", 3: "/ebook", 4: "/screen"}

   # Basic controls
    reader = PdfReader(input_file_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)
    file_path = "inputFile.pdf"
    with open(file_path, "wb") as f:
        writer.write(f)

    # Check if valid path
    if not os.path.isfile(file_path):
        print("Error: invalid path for input PDF file.", file_path)
        sys.exit(1)

    # Check if file is a PDF by extension
    if file_path.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file is not a PDF.", file_path)
        sys.exit(1)

    gs = get_ghostscript_path()
    init_size = os.path.getsize(file_path)
    # Convert bytes to kilobytes the initial size
    initial_size = init_size / 1000
    
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(output_file_path),
            file_path,
        ]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / init_size)
    final_ratio = ratio * 100
    # print("Compression by {0:.0%}.".format(ratio))
    # print("Final file size is {0:.3f}MB".format(final_size / 1000000))
    # print("Done.")
    #convert bytes to kilobytes the final size
    final_size = final_size / 1000
    os.remove(file_path)
    return (final_size, final_ratio, initial_size)


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No GhostScript executable was found on path ({'/'.join(gs_names)})"
    )
