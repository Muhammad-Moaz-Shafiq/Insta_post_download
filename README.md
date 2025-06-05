📥 Instagram Media Downloader

A simple yet powerful Python script to download Instagram posts (images/videos) using a profile name , post shortcode , or URL .
🔍 Features

✅ Download media from:

A specific Instagram profile
A single post via its shortcode or URL
Multiple posts via a file containing shortcodes
📁 Each post is saved in a folder named after its shortcode for easy reference.

🔐 Supports private profiles with login capability.

⚙️ No extra metadata files are downloaded — just the media files (image/video).

🛠️ Requirements
Before running the script, ensure you have:

✅ Python 3.x

✅ instaloader library installed

Install Dependencies:

pip install instaloader

📦 Usage

Clone the repository (optional):

git clone https://github.com/Muhammad-Moaz-Shafiq/insta_post_download.git 

cd insta_post_download

Run the script:

🔹 Download posts from a profile

python downloader.py -u YOUR_USERNAME -t TARGET_PROFILE [-c COUNT]

Example:

python downloader.py -u myuser -t nasa -c 5

Downloads the 5 most recent posts from the @nasa Instagram profile.

🔹 Download a single post by shortcode

python downloader.py -s SHORTCODE [-u YOUR_USERNAME]

Example:

python downloader.py -s BxqBZbQlH_9

🔹 Download a post by URL

python downloader.py -P "https://www.instagram.com/p/BxqBZbQlH_9/"  [-u YOUR_USERNAME]

🔹 Batch download multiple posts from a file

Create a file (shortcodes.txt) with one shortcode per line:

BxqBZbQlH_9

ByyKifrFz_0

BwAujJBFz_1

python downloader.py --shortcodes-file shortcodes.txt [-u YOUR_USERNAME]

📁 Output Structure

Each post is downloaded into a separate folder named after the shortcode , like this:

├── ABC123DEF/

│   ├── ABC123DEF.jpg

├── GHI456JKL/

│   ├── GHI456JKL.mp4
