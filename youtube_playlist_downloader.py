import os
import subprocess
import sys
import shutil

# --- Configuration ---
PLAYLIST_URL = "https://www.youtube.com/watch?v=w35CiPqgpVA5"
DOWNLOAD_DIR = "downloads"
# --- End Configuration ---

# Arabic to Latin transliteration map
advanced_arabic_to_latin = {
    'ء': "'", 'آ': "a", 'أ': "a", 'إ': "i",
    'ا': "a", 'ب': "b", 'ت': "t", 'ث': "th",
    'ج': "j", 'ح': "h", 'خ': "kh",
    'د': "d", 'ذ': "dh", 'ر': "r",
    'ز': "z", 'س': "s", 'ش': "sh",
    'ص': "s", 'ض': "d", 'ط': "t",
    'ظ': "z", 'ع': "'", 'غ': "gh",
    'ف': "f", 'ق': "q", 'ك': "k",
    'ل': "l", 'م': "m", 'ن': "n",
    'ه': "h", 'و': "ou", 'ي': "y",
    'ى': "a", 'ة': "h",
    'ً': "", 'ٌ': "", 'ٍ': "",
    'َ': "", 'ُ': "", 'ِ': "",
    'ّ': "", 'ْ': "",
    ' ': " "
}

def advanced_transliterate(arabic_text):
    return ''.join(advanced_arabic_to_latin.get(char, char) for char in arabic_text)

def check_yt_dlp():
    return shutil.which("yt-dlp") is not None

def get_playlist_title(playlist_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--print", "%(playlist_title)s", "--playlist-items", "1", "--no-warnings", playlist_url],
            check=True, capture_output=True, text=True
        )
        title = result.stdout.strip()
        return title if title else "playlist"
    except Exception as e:
        print(f"Error getting playlist title: {e}")
        return "playlist"

def download_playlist_with_yt_dlp(playlist_url, download_dir):
    if not check_yt_dlp():
        print("Error: 'yt-dlp' is not installed.")
        sys.exit(1)

    original_title = get_playlist_title(playlist_url)
    transliterated_title = advanced_transliterate(original_title)
    output_path = os.path.join(download_dir, transliterated_title)

    if not os.path.exists(output_path):
        print(f"Creating download directory: {output_path}")
        os.makedirs(output_path)

    print(f"Downloading playlist: {original_title}")
    print(f"Saving to: {output_path}")

    command = [
        "yt-dlp",
        "-i",
        "--yes-playlist",
        "--progress",
        "--no-simulate",
        "--merge-output-format", "mp4",
        "-f", "best[height<=480][ext=mp4]/best[height<=480]",
        "-o", os.path.join(output_path, "%(playlist_index)02d.%(ext)s"),
        playlist_url
    ]

    try:
        subprocess.run(command, check=True, text=True)
        print("\n✅ Playlist download completed.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ yt-dlp error (code {e.returncode})")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    download_playlist_with_yt_dlp(PLAYLIST_URL, DOWNLOAD_DIR)
