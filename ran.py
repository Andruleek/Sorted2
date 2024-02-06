import os
from pathlib import Path
from shutil import move
from zipfile import ZipFile, BadZipFile


def normalize(filename):
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    normalized_filename = ''.join(mapping.get(char.lower(), char) for char in filename)
    return normalized_filename


def sort_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = Path(root) / filename
            normalized_filename = normalize(filename)
            _, file_extension = os.path.splitext(normalized_filename)
            destination_folder = get_destination_folder(file_extension)

            if not (folder_path / destination_folder).exists():
                (folder_path / destination_folder).mkdir(parents=True, exist_ok=True)

            destination_path = folder_path / destination_folder / normalized_filename
            try:
                move(file_path, destination_path)
            except FileNotFoundError:
                print(f"Failed to move {filename}. File not found.")
            except Exception as e:
                print(f"Failed to move {filename}. Error: {e}")

        # Remove empty directories
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if not os.listdir(dir_path):
                dir_path.rmdir()


def extract_archives(archive_folder):
    for root, dirs, files in os.walk(archive_folder):
        for archive_filename in files:
            archive_path = Path(root) / archive_filename
            _, archive_extension = os.path.splitext(archive_filename)
            normalized_filename = normalize(archive_filename)

            if archive_extension.lower() in ['.zip', '.gz', '.tar']:
                extract_folder = archive_folder / 'archives' / normalized_filename.removesuffix(archive_extension)
                with ZipFile(archive_path, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(extract_folder)
                    except BadZipFile:
                        print(f"Failed to extract {archive_filename} in {archive_folder}. Removing...")
                        archive_path.unlink()

        # Remove empty directories
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if not os.listdir(dir_path):
                dir_path.rmdir()


def get_destination_folder(extension):
    categories = {
        '.jpeg': 'images', '.png': 'images', '.jpg': 'images', '.svg': 'images',
        '.avi': 'videos', '.mp4': 'videos', '.mov': 'videos', '.mkv': 'videos',
        '.doc': 'documents', '.docx': 'documents', '.txt': 'documents', '.pdf': 'documents',
        '.xlsx': 'documents', '.pptx': 'documents',
        '.mp3': 'music', '.ogg': 'music', '.wav': 'music', '.amr': 'music',
        '.zip': 'archives', '.gz': 'archives', '.tar': 'archives'
    }

    return categories.get(extension.lower(), 'others')


def main():
    folder_path = Path("C:/Users/Admin/Desktop/test_garbage_folder_no_nosuffix")
    sort_files(folder_path)
    extract_archives(folder_path / 'archives')
    print("Files sorted successfully.")
    show_results(folder_path)


def show_results(folder_path):
    print("\nFiles in each category:")
    for category in ['images', 'videos', 'documents', 'music', 'archives', 'others']:
        files = list(folder_path.joinpath(category).rglob('*'))
        print(f"{category.capitalize()}: {files}")

    known_extensions = set(['.jpeg', '.png', '.jpg', '.svg', '.avi', '.mp4', '.mov', '.mkv', '.doc', '.docx', '.txt',
                            '.pdf', '.xlsx', '.pptx', '.mp3', '.ogg', '.wav', '.amr', '.zip', '.gz', '.tar'])
    all_extensions = set([os.path.splitext(file)[1].lower() for file in folder_path.rglob('*')])

    unknown_extensions = all_extensions - known_extensions
    print("\nKnown extensions:", known_extensions)
    print("Unknown extensions:", unknown_extensions)


if __name__ == "__main__":
    main()