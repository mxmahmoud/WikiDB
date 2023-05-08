from pathlib import Path
from requests import post


# Function to send a page XML to the server for ingestion
def ingest_page(page_xml, server="127.0.0.1:8000", api="api/v0.1/ingest"):
    headers = {'Content-Type': 'text/plain; charset=utf-8'}
    response = post(f"http://{server}/{api}", data=page_xml.encode('utf-8'), headers=headers)
    response.raise_for_status()


# Function to extract and ingest pages from a Wikipedia dump file
def extract_wiki_dumpfile(archive_path: str = None, ingest_all: bool = False):
    # import packages inside the function just in case they are not needed in other helper functions
    import bz2
    import lxml.etree as ET
    nr_last_entry = 100

    parser = ET.XMLParser(remove_blank_text=True)
    with bz2.open(str(archive_path), 'rb') as f:
        parser = ET.iterparse(f, events=('end',), tag='{*}page')

        # iterate over the pages and ingesting them one by one
        for nr, (_, page_elem) in enumerate(parser):
            ingest_page(ET.tostring(page_elem, encoding="unicode"))

            # clear the page element from memory to conserve resources
            page_elem.clear()

            #show casing the first 100 pages
            if not ingest_all and nr > nr_last_entry:
                break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='A set of tools...')

    # add arguments to the parser
    parser.add_argument('-e', '--extract', dest='extract', action='store_true',
                        help='Extract the bz2 file')
    parser.add_argument('-a', '--archive', dest='archive', required=False,
                        help='Path to the archive file', default = None)
    parser.add_argument('-all', dest='all', required=False, type=bool,
                        help='Load complete archive to database', default = True)

    # parse the arguments
    args = parser.parse_args()

    if args.extract:
        if args.archive == None:
            data_folder = Path(__file__).parent / "data"

            list_of_archives = list(data_folder.glob("*.bz2"))
            if len(list_of_archives) < 1:
                raise("Error: Neither archive has been defined, nor does an archive exist in the folder")
            else:
                print(f"Archive not defined will proceed with archives in the folder as follows:")
                for archive in list_of_archives:
                    print(f"... extracting {archive}")
                    extract_wiki_dumpfile(archive_path = archive, ingest_all = args.all)

        else:
            extract_wiki_dumpfile(archive_path = args.archive, ingest_all = args.all)
    else:
        parser.print_help()

