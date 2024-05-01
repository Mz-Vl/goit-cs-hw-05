import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile

# Login settings
logging.basicConfig(level=logging.ERROR)


async def read_folder(src_folder, dest_folder):
    """
    Recursively reads all files in the source folder and its subfolders,
    and copies them to the appropriate subfolders of the destination folder 
    based on the extension.
    """
    async for entry in src_folder.glob("**/*"):
        if await entry.is_file():
            await copy_file(entry, dest_folder)


async def copy_file(src_file, dest_folder):
    """
    Copies a file to the appropriate subfolder of the destination folder based 
    on its extension.
    """
    try:
        ext = src_file.suffix.lower()
        dest_dir = dest_folder / ext[1:]
        await dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / src_file.name
        await copyfile(src_file, dest_path)
    except Exception as e:
        logging.error(f"Error copying file {src_file}: {e}")


async def main(src_folder, dest_folder):
    """
    The main function that initiates asynchronous reading and copying of files.
    """
    src_folder = AsyncPath(src_folder)
    dest_folder = AsyncPath(dest_folder)
    await read_folder(src_folder, dest_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Asynchronous sorting of files")
    parser.add_argument("src_folder", help="Output folder")
    parser.add_argument("dest_folder", help="Destination folder")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.src_folder, args.dest_folder))
    except Exception as e:
        logging.error(f"Error: {e}")


# To check the program run this command from goit-cs-hw-05/task1 folder:
# python async_prog.py test_folder_task_1 dest_folder_task_1
